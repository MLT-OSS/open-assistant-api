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


def _validate_definition(self, definition: dict) -> bool:
        """
        Validate the structure of the function definition.
        Returns True if valid, False otherwise.
        """
        if "type" not in definition or definition["type"] != "function":
            return False
        
        if "function" not in definition:
            return False
        
        if not isinstance(definition["function"], dict):
            return False
        
        # Check if "name" exists
        if "name" not in definition["function"]:
            return False

        return True
