import openai

from app.models.assistant import Assistant
from app.providers.database import session
from app.services.assistant.assistant import AssistantService


# 测试创建动作
def test_create_assistant():
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
