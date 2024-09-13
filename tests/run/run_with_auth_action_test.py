import time

import openai
import pytest

from app.providers.database import session
from app.schemas.tool.action import ActionBulkCreateRequest
from app.schemas.tool.authentication import Authentication, AuthenticationType
from app.services.tool.action import ActionService


@pytest.fixture
def api_url():
    return "http://127.0.0.1:8086/api/v1/actions"


@pytest.fixture
def create_workspace_with_authentication():
    return {
        "openapi_schema": {
            "openapi": "3.0.0",
            "info": {"title": "Create New Workspace", "version": "1.0.0"},
            "servers": [{"url": "https://tx.c.csvfx.com/api"}],
            "paths": {
                "/tx/v1/workspaces": {
                    "post": {
                        "summary": "Create a new workspace",
                        "description": "This endpoint creates a new workspace with the provided data.",
                        "operationId": "createWorkspace",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string", "description": "The name of the workspace"},
                                            "description": {
                                                "type": "string",
                                                "description": "The description of the workspace",
                                            },
                                            "ui_settings": {
                                                "type": "object",
                                                "properties": {
                                                    "color": {
                                                        "type": "string",
                                                        "description": "The color of the workspace UI",
                                                    },
                                                    "icon": {
                                                        "type": "string",
                                                        "description": "The icon of the workspace UI",
                                                    },
                                                },
                                            },
                                            "tenant_id": {"type": "string", "description": "The tenant ID"},
                                        },
                                    }
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Workspace created successfully",
                                "content": {"application/json": {"schema": {"type": "object", "properties": {}}}},
                            },
                            "401": {"description": "Unauthorized - Authentication credentials are missing or invalid"},
                            "403": {"description": "Forbidden - The authenticated user does not have permission to perform this action"},
                            "500": {"description": "Internal Server Error - Something went wrong on the server side"},
                        },
                    }
                }
            },
        }
    }


# 测试带有action的助手,run 的时候传递自己的auth信息
def test_run_with_action_auth(create_workspace_with_authentication):
    body = ActionBulkCreateRequest(**create_workspace_with_authentication)
    body.authentication = Authentication(type=AuthenticationType.none)
    actions = ActionService.create_actions_sync(session=session, body=body)
    [create_workspace_with_authentication] = actions

    client = openai.OpenAI(base_url="http://localhost:8086/api/v1", api_key="xxx")

    # 创建带有 action 的 assistant
    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="你是一个有用的助手",
        tools=[{"type": "action", "id": create_workspace_with_authentication.id}],
        model="gpt-3.5-turbo-1106",
    )
    print(assistant, end="\n\n")

    thread = client.beta.threads.create()
    print(thread, end="\n\n")

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="在组织63db49f7dcc8bf7b0990903c下,创建一个随机名字的工作空间",
    )
    print(message, end="\n\n")

    run = client.beta.threads.runs.create(
        # model="gpt-3.5-turbo-1106",
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="",
        extra_body={
            "extra_body": {
                "action_authentications": {
                    create_workspace_with_authentication.id: {
                        "type": "bearer",
                        "secret": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2M2RiNDlhY2RjYzhiZjdiMDk5MDhmZDYiLCJhdWQiOiI2M2RiNDlmN2RjYzhiZjdiMDk5MDkwM2MiLCJ1aWQiOiI2M2RiNDlhY2RjYzhiZjdiMDk5MDhmZDYiLCJpYXQiOjE3MTAxNDkxODcsImV4cCI6MTcxMDIzNTU4N30.h96cKhB8rPGKM2PEq6bg4k2j09gR82HCJHUws232Oe4",
                    }
                }
            }
        },
    )
    print(run, end="\n\n")

    while True:
        # run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
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
