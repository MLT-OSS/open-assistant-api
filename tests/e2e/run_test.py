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
        model="gpt-4o",
        response_format={"type": "json_object"},
    )
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "这张图片的场景是什么季节？"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                        }
                    }
                ]
            }
        ],
    )

    thread_message = client.beta.threads.messages.create(
        thread.id,
        role="user",
        content="这张图片中有人物吗？",
    )

    stream = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="请用 json 格式回答",
        additional_messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "这张图片里有什么？"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                        }
                    }
                ]
            }
        ],
        max_completion_tokens=100,
        max_prompt_tokens=100,
        temperature=0.5,
        top_p=0.5,
        stream=True,
    )

    print("\nstream message start")
    for event in stream:
        if event.event == "thread.message.delta":
            print(event.data.delta.content[0].text.value, end="", flush=True)
    print("\nstream message finish")

    query = session.query(Run).filter(Run.thread_id == thread.id)
    run = query.one()
    assert run.instructions == "请用 json 格式回答"
    assert run.model == "gpt-4o"
    query = session.query(Message).filter(Message.thread_id == thread.id).order_by(Message.created_at)
    messages = query.all()
    for message in messages:
        print(message)
    assert run.max_completion_tokens == 100
    assert run.max_prompt_tokens == 100
    assert run.temperature == 0.5
    assert run.top_p == 0.5
    session.close()
