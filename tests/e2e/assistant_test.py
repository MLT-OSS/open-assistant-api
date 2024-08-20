import openai

from app.models.assistant import Assistant
from app.providers.database import session


# 测试创建动作
def test_create_assistant_with_extra_body():
    client = openai.OpenAI(base_url="http://localhost:8086/api/v1", api_key="xxx")
    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="你是一个有用的助手",
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
        # https://platform.openai.com/docs/api-reference/chat/create 具体参数看这里
        model="gpt-3.5-turbo-1106",
    )
    query = session.query(Assistant).filter(Assistant.id == assistant.id)
    assistant = query.one()
    assert assistant.name == "Assistant Demo"
    assert assistant.instructions == "你是一个有用的助手"
    assert assistant.model == "gpt-3.5-turbo-1106"
    assert assistant.extra_body == {
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
    session.close()


# test create assistants with metadata
def test_create_assistant_with_metadata():
    client = openai.OpenAI(base_url="http://localhost:8086/api/v1", api_key="xxx")
    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="你是一个有用的助手",
        metadata={"memory": {"type": "window", "window_size": 2, "max_token_size": 5}},
        model="gpt-3.5-turbo-1106",
    )
    query = session.query(Assistant).filter(Assistant.id == assistant.id)
    assistant = query.one()
    assert assistant.name == "Assistant Demo"
    assert assistant.instructions == "你是一个有用的助手"
    assert assistant.model == "gpt-3.5-turbo-1106"
    assert assistant.metadata_ == {"memory": {"type": "window", "window_size": 2, "max_token_size": 5}}
    session.close()


def test_create_assistant_with_temperature_and_top_p():
    client = openai.OpenAI(base_url="http://localhost:8086/api/v1", api_key="xxx")
    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="你是一个有用的助手",
        temperature=1,
        top_p=1,
        # https://platform.openai.com/docs/api-reference/chat/create 具体参数看这里
        model="gpt-3.5-turbo-1106",
    )
    query = session.query(Assistant).filter(Assistant.id == assistant.id)
    assistant = query.one()
    assert assistant.name == "Assistant Demo"
    assert assistant.instructions == "你是一个有用的助手"
    assert assistant.model == "gpt-3.5-turbo-1106"
    assert assistant.temperature == 1
    assert assistant.top_p == 1
    session.close()


def test_update_assistant_with_temperature_and_top_p():
    client = openai.OpenAI(base_url="http://localhost:8086/api/v1", api_key="xxx")
    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="你是一个有用的助手",
        temperature=1,
        top_p=1,
        # https://platform.openai.com/docs/api-reference/chat/create 具体参数看这里
        model="gpt-3.5-turbo-1106",
    )
    assistant = client.beta.assistants.update(assistant.id, temperature=2, top_p=0.9)
    query = session.query(Assistant).filter(Assistant.id == assistant.id)
    assistant = query.one()
    assert assistant.name == "Assistant Demo"
    assert assistant.instructions == "你是一个有用的助手"
    assert assistant.model == "gpt-3.5-turbo-1106"
    assert assistant.temperature == 2
    assert assistant.top_p == 0.9
    session.close()
