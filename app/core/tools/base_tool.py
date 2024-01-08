from abc import ABC
from typing import Type, Dict, Any, Optional

from langchain.tools import BaseTool as LCBaseTool
from langchain.tools.render import format_tool_to_openai_function
from pydantic import BaseModel, Field


class BaseToolInput(BaseModel):
    """
    Base schema for tool input arguments.
    """

    input: str = Field(..., description="input")


class BaseTool(ABC):
    """
    Base class for tools.

    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        args_schema (Optional[Type[BaseModel]]): The schema for the tool's input arguments.
        openai_function (Dict): The OpenAI function representation of the tool.
    """

    name: str
    description: str

    args_schema: Optional[Type[BaseModel]] = BaseToolInput

    openai_function: Dict

    def __init_subclass__(cls) -> None:
        lc_tool = LCTool(name=cls.name, description=cls.description, args_schema=cls.args_schema, _run=lambda x: x)
        cls.openai_function = {"type": "function", "function": dict(format_tool_to_openai_function(lc_tool))}

    def configure(self, **kwargs):
        """
        Configure the tool with the provided keyword arguments.

        Args:
            **kwargs: Additional configuration parameters.
        """
        return

    def run(self, **kwargs) -> Any:
        """
        Executes the tool with the given arguments.

        Args:
            **kwargs: Additional keyword arguments for the tool.

        Returns:
            Any: The result of executing the tool.
        """
        raise NotImplementedError()

    def instruction_supplement(self) -> str:
        """
        Provides additional instructions to supplement the run instruction for the tool.

        Returns:
            str: The additional instructions.
        """
        return ""


class LCTool(LCBaseTool):
    name: str = ""
    description: str = ""

    def _run(self):
        pass
