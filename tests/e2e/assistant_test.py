import openai

from app.api.deps import get_session
from app.services.assistant.assistant import AssistantService


# 测试创建动作
def test_create_assistant():
    client = openai.OpenAI(base_url="http://localhost:8086/api/v1", api_key="xxx")
    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="你是一个有用的助手",
        extra_body={
            "extra_body": {
                "frequency_penalty": 0,
                "logit_bias": None,
                "logprobs": True,
                "top_logprobs": 0,
                "max_tokens": 1024,
                "presence_penalty": 0.6,
                "temperature": 1,
                "n": 1,
                "presence_penalty": 0,
                "top_p": 1,
            }
        },
        # https://platform.openai.com/docs/api-reference/chat/create 具体参数看这里
        model="gpt-3.5-turbo-1106",
    )
    session = next(get_session())
    assistant = AssistantService.get_assistant(session=session, assistant_id=assistant.id)
    assert assistant.name == "Assistant Demo"
    assert assistant.instructions == "你是一个有用的助手"
    assert assistant.model == "gpt-3.5-turbo-1106"
    assert assistant.extra_body == {
        "frequency_penalty": 0,
        "logit_bias": None,
        "logprobs": True,
        "top_logprobs": 0,
        "max_tokens": 1024,
        "presence_penalty": 0.6,
        "temperature": 1,
        "n": 1,
        "presence_penalty": 0,
        "top_p": 1,
    }
