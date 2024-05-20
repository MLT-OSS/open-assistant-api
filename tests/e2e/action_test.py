import json
import requests
import pytest


@pytest.fixture
def api_url():
    return "http://127.0.0.1:8086/api/v1/actions"


@pytest.fixture
def valid_payload():
    return {
        "openapi_schema": {
            "openapi": "3.0.0",
            "info": {
                "title": "OpenWeatherMap One Call API",
                "description": "API for accessing comprehensive weather data from OpenWeatherMap.",
                "version": "1.0.0",
            },
            "servers": [
                {
                    "url": "https://api.openweathermap.org/data/3.0",
                    "description": "OpenWeatherMap One Call API server",
                }
            ],
            "paths": {
                "/onecall": {
                    "get": {
                        "summary": "Get Comprehensive Weather Data",
                        "description": "Retrieves weather data for a specific latitude and longitude.",
                        "operationId": "get_weather_data",
                        "parameters": [
                            {
                                "in": "query",
                                "name": "lat",
                                "schema": {"type": "number", "format": "float", "minimum": -90, "maximum": 90},
                                "required": True,
                                "description": "Latitude, decimal (-90 to 90).",
                            },
                            {
                                "in": "query",
                                "name": "lon",
                                "schema": {"type": "number", "format": "float", "minimum": -180, "maximum": 180},
                                "required": True,
                                "description": "Longitude, decimal (-180 to 180).",
                            },
                            {
                                "in": "query",
                                "name": "exclude",
                                "schema": {"type": "string"},
                                "required": False,
                                "description": "Exclude some parts of the weather data(current, minutely, hourly, daily, alerts).",
                            },
                            {
                                "in": "query",
                                "name": "appid",
                                "schema": {"type": "string", "enum": ["101f41d3ff4095824722d57a513cb80a"]},
                                "required": True,
                                "description": "Your unique API key.",
                            },
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful response with comprehensive weather data.",
                                "content": {"application/json": {"schema": {"type": "object", "properties": {}}}},
                            }
                        },
                    }
                }
            },
        }
    }


@pytest.fixture
def created_action_id(api_url, valid_payload):
    # 在创建动作的 fixture 中执行创建动作并返回动作 ID
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, headers=headers, json=valid_payload)
    assert response.status_code == 200
    return response.json()[0]["id"]


# 测试创建动作
def test_create_action(api_url, valid_payload):
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, headers=headers, json=valid_payload)
    assert response.status_code == 200


# 测试获取动作
def test_get_action(api_url, created_action_id):
    get_url = f"{api_url}/{created_action_id}"
    response = requests.get(get_url)
    assert response.status_code == 200


# 测试更新动作
def test_update_action(api_url, valid_payload, created_action_id):
    update_url = f"{api_url}/{created_action_id}"
    valid_payload["openapi_schema"]["paths"]["/onecall"]["get"]["operationId"] = "update_test"
    headers = {"Content-Type": "application/json"}
    response = requests.post(update_url, headers=headers, json=valid_payload)
    assert response.status_code == 200
    assert response.json()["operation_id"] == "update_test"


# 测试删除动作
def test_delete_action(api_url, created_action_id):
    delete_url = f"{api_url}/{created_action_id}"
    response = requests.delete(delete_url)
    assert response.status_code == 200


# 测试删除动作
def test_run_action(api_url, created_action_id):
    run_action_url = f"{api_url}/{created_action_id}/run"
    payload = json.dumps({"parameters": {"lon": 120.1552, "lat": 30.2741}})
    headers = {"Content-Type": "application/json"}
    response = requests.post(run_action_url, headers=headers, data=payload)

    assert response.status_code == 200
