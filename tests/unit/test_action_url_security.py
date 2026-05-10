import socket

from app.exceptions.exception import ValidateFailedError
from app.schemas.tool.action import ActionBodyType, ActionMethod, validate_openapi_schema
from app.schemas.tool.authentication import Authentication, AuthenticationType
from app.services.tool.openapi_call import call_action_api
from app.services.tool.url_security import UnsafeActionURLError, validate_action_url


def _addrinfo(address):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (address, 80))]


def _schema(server_url):
    return {
        "openapi": "3.0.0",
        "info": {"title": "test", "version": "1.0"},
        "servers": [{"url": server_url}],
        "paths": {
            "/status": {
                "get": {
                    "operationId": "get_status",
                    "description": "read status",
                    "responses": {"200": {"description": "ok"}},
                }
            }
        },
    }


class FakeResponse:
    def __init__(self, status_code=200, text="ok", headers=None):
        self.status_code = status_code
        self.text = text
        self.headers = headers or {"Content-Type": "text/plain"}
        self.is_redirect = status_code in {301, 302, 303, 307, 308}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def json(self):
        return {"ok": True}


def test_validate_action_url_blocks_loopback_ip():
    try:
        validate_action_url("http://127.0.0.1:8080/secret")
    except UnsafeActionURLError:
        return
    raise AssertionError("loopback action URL was not blocked")


def test_validate_action_url_blocks_dns_to_private_address(monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", lambda *args, **kwargs: _addrinfo("10.0.0.5"))

    try:
        validate_action_url("https://api.example.test/status")
    except UnsafeActionURLError:
        return
    raise AssertionError("private DNS target was not blocked")


def test_openapi_schema_rejects_private_server_url():
    try:
        validate_openapi_schema(_schema("http://169.254.169.254/latest"))
    except ValidateFailedError:
        return
    raise AssertionError("OpenAPI server URL pointing at metadata service was not rejected")


def test_call_action_api_blocks_private_redirect(monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", lambda host, *args, **kwargs: _addrinfo("93.184.216.34"))

    calls = []

    def fake_request(method, url, **kwargs):
        calls.append((method, url, kwargs))
        return FakeResponse(302, headers={"Location": "http://127.0.0.1:8080/admin"})

    monkeypatch.setattr("app.services.tool.openapi_call.requests.request", fake_request)

    result = call_action_api(
        url="https://api.example.test/status",
        method=ActionMethod.GET,
        path_param_schema={},
        query_param_schema={},
        body_type=ActionBodyType.NONE,
        body_param_schema={},
        parameters={},
        headers={},
        authentication=Authentication(type=AuthenticationType.none),
    )

    assert calls == [("GET", "https://api.example.test/status", calls[0][2])]
    assert result["status"] == 400
    assert "Blocked unsafe action URL" in result["error"]
    assert calls[0][2]["allow_redirects"] is False
    assert calls[0][2]["timeout"] == 10
