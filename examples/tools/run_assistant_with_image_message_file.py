import os
import time
import logging

from pathlib import Path

from examples.prerun import client

if __name__ == "__main__":

    file_path = os.path.join(os.path.dirname(__file__) + "/../../docs/imgs/user.png")
    file = client.files.create(file=Path(file_path), purpose="assistants")

    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="you are a personal assistant, file content could be retrieved to assist the conversation.",
        model="gpt-3.5-turbo-1106",
    )
    logging.info("=====> : %s\n", assistant)

    thread = client.beta.threads.create()
    logging.info("=====> : %s\n", thread)

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="please explain the content in the image file",
        attachments=[{"file_id": file.id}]
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
