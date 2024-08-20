"""
限于 llm 对上下文长度的限制和成本控制，需要对上下文进行筛选整合，本模块用于相关策略描述
"""
from enum import Enum
from typing import List
from abc import ABC, abstractmethod


class MemoryType(str, Enum):
    """
    support 3 kind of context memory
    """

    WINDOW = "window"
    ZERO = "zero"
    NAIVE = "naive"


class Memory(ABC):
    """
    interface for context memory
    """

    @abstractmethod
    def integrate_context(self, messages: List[dict]) -> List[dict]:
        """
        integrate context according to the memory
        """


class WindowMemory(Memory):
    """
    limit the context length to a fixed window size
    """

    def __init__(self, window_size: int = 20, max_token_size: int = 4000):
        if window_size < 1 or max_token_size < 1:
            raise ValueError("window size and max token size should be greater than 0")
        self.window_size = window_size
        self.max_token_size = max_token_size

    def integrate_context(self, messages: List[dict]) -> List[dict]:
        if not messages:
            return []
        histories = messages[-self.window_size :]
        total_length = 0
        for i, message in enumerate(reversed(histories)):
            total_length += len(message["content"])
            if total_length >= self.max_token_size:
                return histories[len(histories) - i - 1 :]
        return histories


class NaiveMemory(Memory):
    """
    navie memory contains all the context
    """

    def integrate_context(self, messages: List[dict]) -> List[dict]:
        return messages


class ZeroMemory(Memory):
    """
    zero memory contains last user message
    """

    def integrate_context(self, messages: List[dict]) -> List[dict]:
        if not messages:
            return []
        for i, message in enumerate(reversed(messages)):
            if message["role"] == "user":
                return messages[len(messages) - i - 1 :]


Memories = {MemoryType.WINDOW: WindowMemory, MemoryType.ZERO: ZeroMemory, MemoryType.NAIVE: NaiveMemory}


def find_memory(assistants_metadata: dict) -> Memory:
    memory_type = assistants_metadata.get("type", MemoryType.NAIVE)
    kwargs = assistants_metadata.copy()
    kwargs.pop("type", None)

    if kwargs:
        return Memories[memory_type](**kwargs)
    else:
        return Memories[memory_type]()
