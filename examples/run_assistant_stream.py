"""
test for stream api
"""
import logging

from openai import AssistantEventHandler
from openai.types.beta import AssistantStreamEvent
from openai.types.beta.assistant_stream_event import ThreadMessageInProgress
from openai.types.beta.threads.message import Message
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta

from examples.prerun import client

class EventHandler(AssistantEventHandler):
    def __init__(self) -> None:
        super().__init__()
    
    def on_tool_call_created(self, tool_call: ToolCall) -> None:
        logging.info("=====> tool call created: %s\n", tool_call)

    def on_tool_call_delta(self, delta: ToolCallDelta, snapshot: ToolCall) -> None:
        logging.info("=====> tool call delta")
        logging.info("delta   : %s", delta)
        logging.info("snapshot: %s\n", snapshot)

    def on_tool_call_done(self, tool_call: ToolCall) -> None:
        logging.info("=====> tool call done: %s\n", tool_call)
        self.tool_call = tool_call

    def on_message_created(self, message: Message) -> None:
        logging.info("=====> message created: %s\n", message)

    def on_message_delta(self, delta, snapshot: Message) -> None:
        logging.info("=====> message delta")
        logging.info("=====> delta   : %s", delta)
        logging.info("=====> snapshot: %s\n", snapshot)

    def on_message_done(self, message: Message) -> None:
        logging.info("=====> message done: %s\n", message)

    def on_text_created(self, text) -> None:
        logging.info("=====> text create: %s\n", text)

    def on_text_delta(self, delta, snapshot) -> None:
        logging.info("=====> text delta")
        logging.info("delta   : %s", delta)
        logging.info("snapshot: %s\n", snapshot)

    def on_text_done(self, text) -> None:
        logging.info("text done: %s\n", text)

    def on_event(self, event: AssistantStreamEvent) -> None:
        if isinstance(event, ThreadMessageInProgress):
            logging.info("event: %s\n", event)


if __name__ == "__main__":
    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="you are a personal assistant, reply 'hello' to user",
        model="gpt-3.5-turbo-1106",
    )
    logging.info("=====> : %s\n", assistant)

    thread = client.beta.threads.create()
    logging.info("=====> : %s\n", thread)

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="hello",
    )
    logging.info("=====> : %s\n", message)

    event_handler = EventHandler()
    with client.beta.threads.runs.create_and_stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        event_handler=event_handler,
        extra_body={
            "stream_options": {"include_usage": True}
        }
    ) as stream:
        stream.until_done()