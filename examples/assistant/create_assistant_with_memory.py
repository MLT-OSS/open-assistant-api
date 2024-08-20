import logging

from examples.prerun import client

if __name__ == "__main__":
    # support three types of memory: navie, zero, window
    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="you are a personal assistant, reply 'hello' to user",
        model="gpt-3.5-turbo-1106",
        metadata={"memory": {"type": "naive"}}
        # metadata={"memory": {"type": "zero"}}
        # metadata={"memory": {"type": "window", "window_size": 5}}
    )
    logging.info("=====> : %s\n", assistant)
