from app.models.action import Action
from app.core.tools.base_tool import BaseTool
from app.exceptions.exception import ResourceNotFoundError
from app.services.tool.openapi_call import call_action_api
from app.schemas.tool.action import ActionMethod, ActionBodyType
from app.services.tool.openapi_utils import action_param_dict_to_schema
from app.schemas.tool.authentication import Authentication


class OpenapiFunctionTool(BaseTool):
    """
    openapi tool, definition as follows:
    {'id': '65d6c295a09d481250cc8ed1', 'type': 'action'}
    """

    name = ""
    description = ""
    args_schema = None
    action: Action = None

    def __init__(self, definition: dict, extra_body: dict, action: Action) -> None:
        if definition["type"] != "action" or "id" not in definition:
            raise ValueError(f"definition format error: {definition}")
        # an exception is thrown if no action is found
        if action is None:
            raise ResourceNotFoundError(message="action not found")
        if not action.use_for_everyone:
            action_authentications = extra_body.get("action_authentications")
            if action_authentications:
                authentication = action_authentications.get(action.id)
                if authentication:
                    action.authentication = authentication
                else:
                    action.authentication = {"type": "none"}
        self.action = action
        self.openai_function = {"type": "function", "function": action.function_def}
        self.name = action.function_def["name"]

    def run(self, **arguments: dict) -> dict:
        action = self.action
        response = call_action_api(
            url=action.url,
            method=ActionMethod(action.method),
            path_param_schema=action_param_dict_to_schema(action.path_param_schema),
            query_param_schema=action_param_dict_to_schema(action.query_param_schema),
            body_param_schema=action_param_dict_to_schema(action.body_param_schema),
            body_type=ActionBodyType(action.body_type),
            parameters=arguments,
            headers={},
            authentication=Authentication(**action.authentication),
        )
        return response
