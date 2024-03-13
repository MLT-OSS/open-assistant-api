from enum import Enum
from typing import List

from sqlmodel import select

from app.api.deps import get_session
from app.exceptions.exception import ServerError
from app.models.action import Action
from app.core.tools.base_tool import BaseTool
from app.core.tools.external_function_tool import ExternalFunctionTool
from app.core.tools.openapi_function_tool import OpenapiFunctionTool
from app.core.tools.retrieval import RetrievalTool
from app.core.tools.web_search import WebSearchTool


class AvailableTools(str, Enum):
    RETRIEVAL = "retrieval"
    WEB_SEARCH = "web_search"


TOOLS = {
    AvailableTools.RETRIEVAL: RetrievalTool,
    AvailableTools.WEB_SEARCH: WebSearchTool,
}


def find_tools(run, session=next(get_session())) -> List[BaseTool]:
    action_ids = [tool.get("id") for tool in run.tools if tool.get("type") == "action"]
    actions = session.exec(select(Action).where(Action.id.in_(action_ids))).all()
    action_map = {action.id: action for action in actions}

    tools = []
    for tool in run.tools:
        tool_name = tool["type"]
        if tool_name in TOOLS:
            tools.append(TOOLS[tool_name]())
        elif tool_name == "function":
            tools.append(ExternalFunctionTool(tool))
        elif tool_name == "action":
            action = action_map.get(tool.get("id"))
            tools.append(OpenapiFunctionTool(tool, run.extra_body, action))
        else:
            raise ServerError(f"Unknown tool type {tool}")
    return tools
