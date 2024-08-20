import time
import logging
import requests
import json

from app.exceptions.exception import BadRequestError
from examples.prerun import client
from examples.prerun import base_url
from examples.prerun import api_key


# To test the localhost, you can listen to a port using the shell command 'echo -e "HTTP/1.1 200 OK\r\n\r\n Success" | nc -l 9999'.
# Make sure to change the URL to match your API server.
auth_server_url = "http://localhost:9999/api/v1"

def create_worksapce_action():
    """
    create action with actions api
    """
    openapi_schema = {
        "openapi_schema": {
            "openapi": "3.0.0",
            "info": {"title": "Create New Workspace", "version": "1.0.0"},
            "servers": [{"url": f"{auth_server_url}"}],
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
                            "403": {
                                "description": "Forbidden - The authenticated user does not have permission to perform this action"
                            },
                            "500": {"description": "Internal Server Error - Something went wrong on the server side"},
                        },
                    }
                }
            },
        }
    }
    openapi_schema["authentication"] = {"type": "none"}
    actions_url = f"{base_url}/actions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.request("POST", actions_url, headers=headers, data=json.dumps(openapi_schema), timeout=1000)
    if response.status_code != 200:
        raise BadRequestError(f"Failed to create action: {response.text}")
    return response.json()


if __name__ == "__main__":
    [create_workspace_with_authentication] = create_worksapce_action()
    logging.info("=====> action: %s\n", create_workspace_with_authentication)

    # create a assistant with action
    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="you are a personal assistant",
        tools=[{"type": "action", "id": create_workspace_with_authentication["id"]}],
        model="gpt-3.5-turbo-1106",
    )
    logging.info("=====> : %s\n", assistant)

    thread = client.beta.threads.create()
    logging.info("=====> : %s\n", thread)

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="在组织 63db49f7dcc8bf7b0990903c 下, 创建一个随机名字的工作空间",
    )
    logging.info("=====> : %s\n", message)

    # create a run with auth info
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="",
        extra_body={
            "extra_body": {
                "action_authentications": {
                    create_workspace_with_authentication["id"]: {
                        # auth info, change as needed
                        "type": "bearer",
                        "secret": "xxx",
                    }
                }
            }
        },
    )
    logging.info("=====> : %s\n", run)

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)

            logging.info("=====> messages:")
            for message in messages:
                assert message.content[0].type == "text"
                logging.info("%s", {"role": message.role, "message": message.content[0].text.value})
            break
        elif run.status == "failed":
            logging.error("run failed %s\n", run.last_error)
            break
        else:
            logging.info("in progress...\n")
            time.sleep(5)
