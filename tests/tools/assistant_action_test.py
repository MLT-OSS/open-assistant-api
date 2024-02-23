import requests
import pytest
import openai
from app.services.tool.action import ActionService
from app.api.deps import get_session
from app.schemas.tool.action import ActionBulkCreateRequest
from app.schemas.tool.authentication import Authentication, AuthenticationType
import time


@pytest.fixture
def api_url():
    return "http://127.0.0.1:8086/api/v1/actions"


@pytest.fixture
def get_weather_data_valid_payload():
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
def get_number_fact_valid_payload():
    return {
        "openapi_schema": {
            "openapi": "3.0.0",
            "info": {
                "title": "Numbers API",
                "version": "1.0.0",
                "description": "API for fetching interesting number facts",
            },
            "servers": [{"url": "http://numbersapi.com"}],
            "paths": {
                "/{number}": {
                    "get": {
                        "description": "Get fact about a number",
                        "operationId": "get_number_fact",
                        "parameters": [
                            {
                                "name": "number",
                                "in": "path",
                                "required": True,
                                "description": "The number to get the fact for",
                                "schema": {"type": "integer"},
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "A fact about the number",
                                "content": {"text/plain": {"schema": {"type": "string"}}},
                            }
                        },
                    }
                }
            },
        }
    }


# 测试带有action的助手
def test_assistant_with_action_tools(get_weather_data_valid_payload, get_number_fact_valid_payload):
    # get_weather_data
    session = next(get_session())
    body = ActionBulkCreateRequest(**get_weather_data_valid_payload)
    body.authentication = Authentication(
        type=AuthenticationType.none,
    )
    actions = ActionService.create_actions(session=session, body=body)
    [get_weather_data] = actions
    # get_number_fact
    body = ActionBulkCreateRequest(**get_number_fact_valid_payload)
    body.authentication = Authentication(
        type=AuthenticationType.none,
    )
    actions = ActionService.create_actions(session=session, body=body)
    [get_number_fact] = actions
    client = openai.OpenAI(
        base_url="http://localhost:8086/api/v1", api_key="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"
    )
    # 创建带有 action 的 assistant
    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="你是一个有用的助手",
        tools=[
            {"type": "action", "id": get_weather_data.id},
            {"type": "action", "id": get_number_fact.id},
        ],
        model="gpt-3.5-turbo-1106",
    )
    print(assistant, end="\n\n")

    thread = client.beta.threads.create()
    print(thread, end="\n\n")

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="随机给我一个数字, 使用get_number_fact工具得到结果, 然后翻译成中文",
    )
    print(message, end="\n\n")

    run = client.beta.threads.runs.create(
        # model="gpt-3.5-turbo-1106",
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="",
    )
    print(run, end="\n\n")

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "completed":
            print("done!", end="\n\n")
            messages = client.beta.threads.messages.list(thread_id=thread.id)

            print("messages: ")
            for message in messages:
                assert message.content[0].type == "text"
                print(messages)
                print({"role": message.role, "message": message.content[0].text.value})

            break
        else:
            print("\nin progress...")
            time.sleep(1)
