import logging
from typing import List

from openai import OpenAI
from openai import Stream
from openai.types.chat import ChatCompletionChunk, ChatCompletion

from config.llm import LLMSettings


class LLMBackend:
    """
    openai chat 接口封装
    """

    def __init__(self, llm_settings: LLMSettings) -> None:
        self.base_url = llm_settings.OPENAI_API_BASE if llm_settings.OPENAI_API_BASE else None
        self.api_key = llm_settings.OPENAI_API_KEY
        self.client = OpenAI(
          api_key=self.api_key,
          base_url=self.base_url
        )

    def run(
        self, messages: List, model: str, tools: List = None, tool_choice="auto", stream=False
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        chat_params = {
            "messages": messages,
            "model": model,
            "stream": stream,
        }
        if tools:
            chat_params['tools'] = tools
            chat_params['tool_choice'] = tool_choice if tool_choice else "auto"
        logging.info(f"chat_params: {chat_params}")
        response = self.client.chat.completions.create(**chat_params)
        logging.info(f"chat_response: {response}")
        return response
