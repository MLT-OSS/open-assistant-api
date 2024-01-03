"""
限于 llm 对上下文长度的限制和成本控制，需要对上下文进行筛选整合，本模块用于相关策略描述
"""
from abc import ABC, abstractmethod
from typing import List


class ContextIntegrationPolicy(ABC):
    """
    整合策略接口
    """
    @abstractmethod
    def integrate_context(self, messages: List[dict]) -> List[dict]:
        """
        对 message 信息进行筛选处理
        """


class DefaultContextIntegrationPolicy(ContextIntegrationPolicy):
    """
    默认不进行处理
    """
    def integrate_context(self, messages: List[dict]) -> List[dict]:
        return messages


context_integration_policy = DefaultContextIntegrationPolicy()
