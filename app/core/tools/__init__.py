from enum import Enum
from app.core.tools.base_tool import BaseTool
from app.core.tools.external_function_tool import ExternalFunctionTool
from app.api.deps import get_session

from app.core.tools.retrieval import RetrievalTool
from app.core.tools.web_search import WebSearchTool
from app.exceptions.exception import ServerError
from app.core.tools.openapi_function_tool import OpenapiFunctionTool
from typing import List


class AvailableTools(str, Enum):
    RETRIEVAL = "retrieval"
    WEB_SEARCH = "web_search"


TOOLS = {
    AvailableTools.RETRIEVAL: RetrievalTool,
    AvailableTools.WEB_SEARCH: WebSearchTool,
}


def tool_find(tool, tool_name_fetcher=lambda tool: tool, session=next(get_session())) -> BaseTool:
    tool_name = tool_name_fetcher(tool)
    if tool_name in TOOLS:
        return TOOLS[tool_name]()
    elif tool_name == "function":
        return ExternalFunctionTool(tool)
    elif tool_name == "action":
        return OpenapiFunctionTool(tool, session)
    else:
        raise ServerError(f"Unknown tool type {tool}")


def filter_delete_tools(tools) -> List[BaseTool]:
    return [tool for tool in tools if not (isinstance(tool, OpenapiFunctionTool) and tool.is_deleted)]
