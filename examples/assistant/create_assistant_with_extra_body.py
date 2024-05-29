import logging

from examples.prerun import client

if __name__ == "__main__":
    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="you are a personal assistant, reply 'hello' to user",
        model="gpt-3.5-turbo-1106",
        extra_body={
            "extra_body": {
                "model_params": {
                    "frequency_penalty": 0,
                    "logit_bias": None,
                    "max_tokens": 1024,
                    "temperature": 1,
                    "presence_penalty": 0,
                    "top_p": 1,
                }
            }
        },
    )
    logging.info("=====> : %s\n", assistant)