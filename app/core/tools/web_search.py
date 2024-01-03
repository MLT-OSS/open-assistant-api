from typing import Type

from langchain.utilities import BingSearchAPIWrapper
from pydantic import BaseModel, Field

from app.core.tools.base_tool import BaseTool
from config.llm import tool_settings


class WebSearchToolInput(BaseModel):
    query: str = Field(
        ...,
        description="Search query. Use a format suitable for Bing and, if necessary, "
        "use Bing's advanced search function",
    )


class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = (
        "A tool for performing a Bing search and extracting snippets and webpages "
        "when you need to search for something you don't know or when your information "
        "is not up to date. "
        "Input should be a search query."
    )

    args_schema: Type[BaseModel] = WebSearchToolInput

    _bing_search_api_wrapper = BingSearchAPIWrapper(
        bing_search_url=tool_settings.BING_SEARCH_URL,
        bing_subscription_key=tool_settings.BING_SUBSCRIPTION_KEY,
        k=tool_settings.WEB_SEARCH_NUM_RESULTS,
    )

    def run(self, query: str) -> dict:
        return self._bing_search_api_wrapper.results(query=query, num_results=tool_settings.WEB_SEARCH_NUM_RESULTS)
