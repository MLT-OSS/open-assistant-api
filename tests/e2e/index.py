import os
import time
from pathlib import Path

import openai
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput

if __name__ == "__main__":
    client = openai.OpenAI(
        base_url="http://localhost:8086/api/v1", api_key="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"
    )

    file_path = os.path.join(os.path.dirname(__file__) + "/../../README.md")
    file = client.files.create(file=Path(file_path), purpose="assistants")

    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="你是一个有用的助手",
        tools=[
            {"type": "web_search"},
            {"type": "retrieval"},
            {
                "type": "function",
                "function": {
                    "name": "calculator",
                    "description": "计算器, 需要数学计算时必须使用此工具",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "input": {
                                "type": "string",
                                "description": "需要计算的算术表达式",
                            }
                        },
                        "required": ["input"],
                    },
                },
            },
        ],
        file_ids=[file.id],
        model="gpt-3.5-turbo-1106",
        # model="gpt-4-1106-preview",
    )
    print(assistant, end="\n\n")

    thread = client.beta.threads.create()
    print(thread, end="\n\n")

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="iphone15 256g 和 iphone15 pro 512g 价格分别是多少, 使用calculator工具计算两者总共的价格",  # multi web_search + calculator
        # content="Open Assistant Api 是什么",  # retrieval
    )
    print(message, end="\n\n")

    run = client.beta.threads.runs.create(
        # model="gpt-3.5-turbo-1106",
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="",
    )
    print(run, end="\n\n")

    print("checking assistant status. ")
    # while True:
    #     run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    #     run_steps = client.beta.threads.runs.steps.list(run_id=run.id, thread_id=thread.id).data
    #     for run_step in run_steps:
    #         print(run_step)
    #         tool_calls = run_step.step_details.type == "tool_calls" and run_step.step_details.tool_calls
    #         if run.status == "requires_action" and run_step.status == "in_progress" and tool_calls:
    #             for tool_call in tool_calls:
    #                 try:
    #                     client.beta.threads.runs.submit_tool_outputs(
    #                         run_id=run.id,
    #                         thread_id=thread.id,
    #                         # fake output
    #                         tool_outputs=[ToolOutput(output="666", tool_call_id=tool_call.id)],
    #                     )
    #                 except Exception:
    #                     pass

    #     run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    #     if run.status == "completed":
    #         print("done!", end="\n\n")
    #         messages = client.beta.threads.messages.list(thread_id=thread.id)

    #         print("messages: ")
    #         for message in messages:
    #             assert message.content[0].type == "text"
    #             print(messages)
    #             print({"role": message.role, "message": message.content[0].text.value})

    #         # delete asst
    #         # client.beta.assistants.delete(assistant.id)

    #         break
    #     else:
    #         print("\nin progress...")
    #         time.sleep(5)
