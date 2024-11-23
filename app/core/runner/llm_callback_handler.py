import logging


from openai import Stream
from openai.types.chat import ChatCompletionChunk, ChatCompletionMessage

from app.core.runner.pub_handler import StreamEventHandler
from app.core.runner.utils import message_util


class LLMCallbackHandler:
    """
    LLM chat callback handler, handling message sending and message merging
    """

    def __init__(
        self, run_id: str, on_step_create_func, on_message_create_func, event_handler: StreamEventHandler
    ) -> None:
        super().__init__()
        self.run_id = run_id
        self.final_message_started = False
        self.on_step_create_func = on_step_create_func
        self.step = None
        self.on_message_create_func = on_message_create_func
        self.message = None
        self.event_handler: StreamEventHandler = event_handler

    def handle_llm_response(
        self,
        response_stream: Stream[ChatCompletionChunk],
    ) -> ChatCompletionMessage:
        """
        Handle LLM response stream
        :param response_stream: ChatCompletionChunk stream
        :return: ChatCompletionMessage
        """
        message = ChatCompletionMessage(content="", role="assistant", tool_calls=[])

        index = 0
        try:
            for chunk in response_stream:
                logging.debug(chunk)

                if chunk.usage:
                    self.event_handler.pub_message_usage(chunk)
                    continue

                if not chunk.choices:
                    continue

                choice = chunk.choices[0]
                delta = choice.delta

                if not delta:
                    continue

                # merge tool call delta
                if delta.tool_calls:
                    for tool_call_delta in delta.tool_calls:
                        message_util.merge_tool_call_delta(message.tool_calls, tool_call_delta)

                elif delta.content:
                    # call on delta message received
                    if not self.final_message_started:
                        self.final_message_started = True

                        self.message = self.on_message_create_func(content="")
                        self.step = self.on_step_create_func(self.message.id)
                        logging.debug("create message and step (%s), (%s)", self.message, self.step)

                        self.event_handler.pub_run_step_created(self.step)
                        self.event_handler.pub_run_step_in_progress(self.step)
                        self.event_handler.pub_message_created(self.message)
                        self.event_handler.pub_message_in_progress(self.message)

                    # append message content delta
                    message.content += delta.content
                    self.event_handler.pub_message_delta(self.message.id, index, delta.content, delta.role)
        except Exception as e:
            logging.error("handle_llm_response error: %s", e)
            raise e

        return message
