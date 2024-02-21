import logging

from openai import Stream
from openai.types.chat import ChatCompletionChunk, ChatCompletionMessage

from app.core.runner import pub_handler
from app.core.runner.utils import message_util


class LLMCallbackHandler:
    """
    LLM chat callback handler, handling message sending and message merging
    """

    def __init__(self, run_id: str, on_final_message_start_func=None) -> None:
        super().__init__()
        self.run_id = run_id
        self.final_message_started = False
        self.on_final_message_start_func = on_final_message_start_func
        self.on_final_message_start_func_output = None

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
        channel = pub_handler.generate_channel_name(self.run_id)

        try:
            for chunk in response_stream:
                logging.debug(chunk)

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
                    # append message content delta
                    message.content += delta.content
                    pub_handler.pub_event(channel, {"type": "data", "data": chunk.json(ensure_ascii=False)})

                    # call on final message start func
                    if self.on_final_message_start_func and not self.final_message_started:
                        self.final_message_started = True
                        self.on_final_message_start_func_output = self.on_final_message_start_func()

            if not message.tool_calls:
                pub_handler.pub_event(channel, {"type": "end"})

        except Exception as e:
            logging.exception(e)
            pub_handler.pub_event(channel, {"type": "error", "data": str(e)})

        return message
