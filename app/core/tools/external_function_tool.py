from app.core.tools.base_tool import BaseTool


class ExternalFunctionTool(BaseTool):
    """
    external tool, definition as follows:
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "parameters": {
                "type": "object",
                "required": ["input"],
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "需要计算的算术表达式"
                    }
                }
            },
            "description": "计算器"
        }
    }
    """

    # for disable BaseTool.__init_subclass__
    name = ""
    description = ""
    args_schema = None

    def __init__(self, definition: dict) -> None:
        if definition["type"] != "function" or "function" not in definition:
            raise ValueError(f"definition format error: {definition}")

        # 其它参数未使用到，暂时不做处理
        self.openai_function = definition
        self.name = definition["function"]["name"]
