import logging
from typing import List

import openai
from openai.types.chat import ChatCompletionMessage

from config.llm import LLMSettings


class LLMBackend:
    """
    openai chat 接口封装
    """

    def __init__(self, llm_settings: LLMSettings) -> None:
        openai.base_url = llm_settings.OPENAI_API_BASE + "/" if llm_settings.OPENAI_API_BASE else None
        openai.api_key = llm_settings.OPENAI_API_KEY

    def run(self, messages: List, model: str, tools: List = None, tool_choice="auto") -> ChatCompletionMessage:
        chat_params = {
            "messages": messages,
            "model": model,
            "tools": tools if tools else None,
            "tool_choice": tool_choice if tools else None,
        }
        logging.info(f"chat_params: {chat_params}")
        response = openai.chat.completions.create(**chat_params)
        return response.choices[0].message
