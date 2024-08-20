import time
import logging

from app.schemas.runs import ToolOutput
from examples.prerun import client

if __name__ == "__main__":

    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="you are a personal math assistant, can use calculator tool to solve math problems",
        model="gpt-3.5-turbo-1106",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "calculator",
                    "description": "can solve math problems, use this tool when you need to calculate.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "input": {
                                "type": "string",
                                "description": "the arithmetic expression to be calculated.",
                            }
                        },
                        "required": ["input"],
                    },
                },
            },
        ]
    )
    logging.info("=====> : %s\n", assistant)

    thread = client.beta.threads.create()
    logging.info("=====> : %s\n", thread)

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="what is 1+1?",
    )
    logging.info("=====> : %s\n", message)

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="",
    )
    logging.info("=====> : %s\n", run)

    logging.info("checking assistant status. \n")
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        run_steps = client.beta.threads.runs.steps.list(run_id=run.id, thread_id=thread.id).data
        for run_step in run_steps:
            logging.info("=====> : %s\n", run_step)
            tool_calls = run_step.step_details.type == "tool_calls" and run_step.step_details.tool_calls

            if run.status == "requires_action" and run_step.status == "in_progress" and tool_calls:
                for tool_call in tool_calls:
                    try:
                        client.beta.threads.runs.submit_tool_outputs(
                            run_id=run.id,
                            thread_id=thread.id,
                            # we submit a fake output here, you can replace it with the real output
                            tool_outputs=[ToolOutput(output="2", tool_call_id=tool_call.id)],
                        )
                    except Exception:
                        pass

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)

            logging.info("=====> messages:")
            for message in messages:
                assert message.content[0].type == "text"
                logging.info("%s", {"role": message.role, "message": message.content[0].text.value})

            # delete asst
            client.beta.assistants.delete(assistant.id)
            break
        elif run.status == "failed":
            logging.error("run failed %s\n", run.last_error)
            break
        else:
            logging.info("in progress...\n")
            time.sleep(5)
