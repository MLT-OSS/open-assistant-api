import time

import openai

from app.api.deps import get_session
from app.schemas.tool.action import ActionBulkCreateRequest
from app.schemas.tool.authentication import Authentication, AuthenticationType
from app.services.tool.action import ActionService


def test_run_with_assistant_extra_body():
    client = openai.OpenAI(base_url="http://localhost:8086/api/v1", api_key="xxx")
    # 创建带有 action 的 assistant
    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="你是一个有用的助手",
        model="gpt-3.5-turbo-1106",
        extra_body={
            "extra_body": {
                "model_params": {
                    "frequency_penalty": 0,
                    "logit_bias": None,
                    "max_tokens": 1024,
                    "presence_penalty": 0.6,
                    "temperature": 1,
                    "presence_penalty": 0,
                    "top_p": 1,
                }
            }
        },
    )
    print(assistant, end="\n\n")

    thread = client.beta.threads.create()
    print(thread, end="\n\n")

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="你好,介绍一下你自己",
    )
    print(message, end="\n\n")

    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id, instructions="")
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
