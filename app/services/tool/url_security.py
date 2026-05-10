import ipaddress
import socket
import urllib.parse
from typing import Iterable

from app.exceptions.exception import ValidateFailedError


_ALLOWED_ACTION_SCHEMES = {"http", "https"}
_BLOCKED_HOSTNAMES = {"localhost"}


class UnsafeActionURLError(ValueError):
    pass


def _is_blocked_ip(address: str) -> bool:
    ip = ipaddress.ip_address(address)
    return any(
        [
            ip.is_private,
            ip.is_loopback,
            ip.is_link_local,
            ip.is_multicast,
            ip.is_reserved,
            ip.is_unspecified,
        ]
    )


def _resolved_addresses(hostname: str, port: int | None) -> Iterable[str]:
    try:
        addrinfos = socket.getaddrinfo(hostname, port, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise UnsafeActionURLError(f"Unable to resolve action URL host: {hostname}") from exc

    addresses = set()
    for addrinfo in addrinfos:
        sockaddr = addrinfo[4]
        if sockaddr:
            addresses.add(sockaddr[0])
    return addresses


def validate_action_url(url: str) -> None:
    """Validate that an action URL does not target local or private network addresses."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme.lower() not in _ALLOWED_ACTION_SCHEMES:
        raise UnsafeActionURLError("Action URL scheme must be http or https")

    if not parsed.hostname:
        raise UnsafeActionURLError("Action URL must include a hostname")

    if parsed.username or parsed.password:
        raise UnsafeActionURLError("Action URL must not include user credentials")

    hostname = parsed.hostname.rstrip(".").lower()
    if hostname in _BLOCKED_HOSTNAMES or hostname.endswith(".localhost"):
        raise UnsafeActionURLError("Action URL host is not allowed")

    try:
        ip = ipaddress.ip_address(hostname)
    except ValueError:
        for address in _resolved_addresses(hostname, parsed.port):
            if _is_blocked_ip(address):
                raise UnsafeActionURLError("Action URL host resolves to a disallowed address")
    else:
        if _is_blocked_ip(str(ip)):
            raise UnsafeActionURLError("Action URL host is not allowed")


def validate_openapi_server_url(url: str) -> None:
    try:
        validate_action_url(url)
    except UnsafeActionURLError as exc:
        raise ValidateFailedError(f"Invalid action server URL: {exc}") from exc
