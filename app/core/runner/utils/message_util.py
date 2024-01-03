"""
This module provides utility functions for working with messages in the OpenAI API.

Functions:
- new_message(role: str, content: str) -> dict: Creates a new message with the specified role and content.
- system_message(content: str) -> dict: Creates a system message with the specified content.
- user_message(content: str) -> dict: Creates a user message with the specified content.
- assistant_message(content: str) -> dict: Creates an assistant message with the specified content.
- tool_calls(tool_calls) -> dict: Creates a message with assistant tool calls.
- tool_call_result(id, content) -> dict: Creates a tool call result message with the specified ID and content.
- is_tool_call(message: ChatCompletionMessage) -> bool: Checks if a message is a tool call.
"""
from typing import List
from openai.types.chat import ChatCompletionMessage


def new_message(role: str, content: str):
    if role != "user" and role != "system" and role != "assistant":
        raise ValueError(f"Invalid role {role}")

    return {"role": role, "content": content}


def system_message(content: str):
    return new_message("system", content)


def user_message(content: str):
    return new_message("user", content)


def assistant_message(content: str):
    return new_message("assistant", content)


def tool_calls(tool_calls):
    return {"role": "assistant", "tool_calls": tool_calls}


def tool_call_result(id, content):
    return {"role": "tool", "tool_call_id": id, "content": content}


def is_tool_call(message: ChatCompletionMessage) -> bool:
    return bool(message.tool_calls)
