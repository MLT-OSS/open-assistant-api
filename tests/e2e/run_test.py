import openai

from app.models.message import Message
from app.models.run import Run
from app.providers.database import session


# 测试创建动作
def test_create_run_with_additional_messages_and_other_parmas():
    client = openai.OpenAI(base_url="http://localhost:8086/api/v1", api_key="xxx")
    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="你是一个有用的助手",
        model="gpt-3.5-turbo-1106",
    )
    thread = client.beta.threads.create()
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="",
        additional_messages=[
            {"role": "user", "content": "100 + 100 等于多少"},
            {"role": "assistant", "content": "100 + 100 等于200"},
            {"role": "user", "content": "如果是乘是多少呢？"},
        ],
        max_completion_tokens=100,
        max_prompt_tokens=100,
        temperature=0.5,
        top_p=0.5,
    )
    query = session.query(Run).filter(Run.id == run.id)
    run = query.one()
    assert run.instructions == "你是一个有用的助手"
    assert run.model == "gpt-3.5-turbo-1106"
    query = session.query(Message).filter(Message.run_id == run.id).order_by(Message.created_at)
    messages = query.all()
    [messgae1, messgae2, messgae3] = messages
    assert messgae1.content == [{"text": {"value": "100 + 100 等于多少", "annotations": []}, "type": "text"}]
    assert messgae1.role == "user"
    assert messgae2.content == [{"text": {"value": "100 + 100 等于200", "annotations": []}, "type": "text"}]
    assert messgae2.role == "assistant"
    assert messgae3.content == [{"text": {"value": "如果是乘是多少呢？", "annotations": []}, "type": "text"}]
    assert messgae3.role == "user"
    assert run.max_completion_tokens == 100
    assert run.max_prompt_tokens == 100
    assert run.temperature == 0.5
    assert run.top_p == 0.5
    session.close()
