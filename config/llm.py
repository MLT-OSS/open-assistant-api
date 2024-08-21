from pydantic.v1 import BaseSettings


class LLMSettings(BaseSettings):
    """
    llm settings
    """

    OPENAI_API_BASE: str = ""
    OPENAI_API_KEY: str = "xxxx"
    LLM_MAX_STEP: int = 25

    class Config(object):
        env_file = ".env"


class ToolSettings(BaseSettings):
    """
    tool settings
    """

    TOOL_WORKER_NUM: int = 10
    TOOL_WORKER_EXECUTION_TIMEOUT: int = 180

    BING_SEARCH_URL: str = "https://api.bing.microsoft.com/v7.0/search"
    BING_SUBSCRIPTION_KEY: str = "xxxx"
    WEB_SEARCH_NUM_RESULTS: int = 5

    R2R_BASE_URL: str = "http://127.0.0.1:8000"
    R2R_USERNAME: str = None
    R2R_PASSWORD: str = None
    R2R_SEARCH_LIMIT: int = 10

    class Config(object):
        env_file = ".env"


tool_settings = ToolSettings()
llm_settings = LLMSettings()
