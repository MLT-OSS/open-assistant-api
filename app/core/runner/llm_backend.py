import logging
from typing import List

from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk, ChatCompletion


class LLMBackend:
    """
    openai chat 接口封装
    """

    def __init__(self, base_url: str, api_key) -> None:
        self.base_url = base_url + "/" if base_url else None
        self.api_key = api_key
        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)

    def run(
        self, messages: List, model: str, tools: List = None, tool_choice="auto", stream=False, extra_body=None
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        chat_params = {
            "messages": messages,
            "model": model,
            "stream": stream,
        }
        if extra_body:
            model_params = extra_body.get("model_params")
            if model_params:
                if "n" in model_params:
                    raise ValueError("n is not allowed in model_params")
                chat_params.update(model_params)
        if tools:
            chat_params["tools"] = tools
            chat_params["tool_choice"] = tool_choice if tool_choice else "auto"
        logging.info("chat_params: %s", chat_params)
        response = self.client.chat.completions.create(**chat_params)
        logging.info("chat_response: %s", response)
        return response
