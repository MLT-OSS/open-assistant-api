from enum import Enum
import re
from typing import Optional, Any, Dict, List

from pydantic import BaseModel, Field, model_validator

import openapi_spec_validator

from app.exceptions.exception import ValidateFailedError
from app.schemas.tool.authentication import Authentication, AuthenticationType


# This function code from the Open Source Project TaskingAI.
# The original code can be found at: https://github.com/TaskingAI/TaskingAI
def validate_openapi_schema(schema: Dict):
    try:
        openapi_spec_validator.validate(schema)
        # check exactly one server in the schema
    except Exception as e:
        if hasattr(e, "message"):
            raise ValidateFailedError(f"Invalid openapi schema: {e.message}")
        else:
            raise ValidateFailedError(f"Invalid openapi schema: {e}")

    if "servers" not in schema:
        raise ValidateFailedError("No server is found in action schema")

    if "paths" not in schema:
        raise ValidateFailedError("No paths is found in action schema")

    if len(schema["servers"]) != 1:
        raise ValidateFailedError("Exactly one server is allowed in action schema")

    # check each path method has a valid description and operationId
    for path, methods in schema["paths"].items():
        for method, details in methods.items():
            if not details.get("description") or not isinstance(details["description"], str):
                if details.get("summary") and isinstance(details["summary"], str):
                    # use summary as its description
                    details["description"] = details["summary"]
                else:
                    raise ValidateFailedError(f"No description is found in {method} {path} in action schema")

            if len(details["description"]) > 512:
                raise ValidateFailedError(
                    f"Description cannot be longer than 512 characters in {method} {path} in action schema"
                )

            if not details.get("operationId") or not isinstance(details["operationId"], str):
                raise ValidateFailedError(f"No operationId is found in {method} {path} in action schema")

            if len(details["operationId"]) > 128:
                raise ValidateFailedError(
                    f"operationId cannot be longer than 128 characters in {method} {path} in action schema"
                )

            if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", details["operationId"]):
                raise ValidateFailedError(
                    f'Invalid operationId {details["operationId"]} in {method} {path} in action schema'
                )

    return schema


# ----------------------------
# Create Action
# POST /actions


# This class utilizes code from the Open Source Project TaskingAI.
# The original code can be found at: https://github.com/TaskingAI/TaskingAI
class ActionBulkCreateRequest(BaseModel):
    openapi_schema: Dict = Field(
        ...,
        description="The action schema is compliant with the OpenAPI Specification. "
        "If there are multiple paths and methods in the schema, "
        "the server will create multiple actions whose schema only has exactly one path and one method",
    )

    authentication: Authentication = Field(
        Authentication(type=AuthenticationType.none), description="The action API authentication."
    )

    use_for_everyone: bool = Field(default=False)

    @model_validator(mode="before")
    def model_validator(cls, data: Any):
        openapi_schema = data.get("openapi_schema")
        validate_openapi_schema(openapi_schema)
        authentication = data.get("authentication")
        if authentication:
            Authentication.model_validate(authentication).encrypt()
        return data


# ----------------------------
# Update Action
# POST /actions/{action_id}


# This class utilizes code from the Open Source Project TaskingAI.
# The original code can be found at: https://github.com/TaskingAI/TaskingAI
class ActionUpdateRequest(BaseModel):
    openapi_schema: Optional[Dict] = Field(
        default=None,
        description="The action schema, which is compliant with the OpenAPI Specification. "
        "It should only have exactly one path and one method.",
    )
    authentication: Optional[Authentication] = Field(None, description="The action API authentication.")

    use_for_everyone: bool = Field(default=False)

    @model_validator(mode="before")
    def model_validator(cls, data: Any):
        if not any([(data.get(key) is not None) for key in ["use_for_everyone", "openapi_schema", "authentication"]]):
            raise ValidateFailedError("At least one field should be filled")
        openapi_schema = data.get("openapi_schema")
        if openapi_schema:
            validate_openapi_schema(openapi_schema)
        authentication = data.get("authentication")
        if authentication:
            Authentication.model_validate(authentication).encrypt()
        return data


# ----------------------------
# Run an Action
# POST /actions/{action_id}/run


# This class utilizes code from the Open Source Project TaskingAI.
# The original code can be found at: https://github.com/TaskingAI/TaskingAI
class ActionRunRequest(BaseModel):
    parameters: Optional[Dict[str, Any]] = Field(None)
    headers: Optional[Dict[str, Any]] = Field(None)


# This class utilizes code from the Open Source Project TaskingAI.
# The original code can be found at: https://github.com/TaskingAI/TaskingAI
class ActionMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    # HEAD = "HEAD"
    # OPTIONS = "OPTIONS"
    # TRACE = "TRACE"
    NONE = "NONE"


# This class utilizes code from the Open Source Project TaskingAI.
# The original code can be found at: https://github.com/TaskingAI/TaskingAI
class ActionParam(BaseModel):
    type: str
    description: str
    enum: Optional[List[str]] = None
    required: bool
    properties: Optional[Dict[str, Dict]] = None

    def is_single_value_enum(self):
        return self.enum and len(self.enum) == 1


# This class utilizes code from the Open Source Project TaskingAI.
# The original code can be found at: https://github.com/TaskingAI/TaskingAI
class ActionBodyType(str, Enum):
    JSON = "JSON"
    FORM = "FORM"
    NONE = "NONE"


# This class utilizes code from the Open Source Project TaskingAI.
# The original code can be found at: https://github.com/TaskingAI/TaskingAI
class ChatCompletionFunctionParametersProperty(BaseModel):
    type: str = Field(
        ...,
        pattern="^(string|number|integer|boolean|object)$",
        description="The type of the parameter.",
    )

    description: str = Field(
        "",
        max_length=256,
        description="The description of the parameter.",
    )

    properties: Optional[Dict] = Field(
        None,
        description="The properties of the parameters.",
    )

    enum: Optional[List[str]] = Field(
        None,
        description="The enum list of the parameter. Which is only allowed when type is 'string'.",
    )


# This class utilizes code from the Open Source Project TaskingAI.
# The original code can be found at: https://github.com/TaskingAI/TaskingAI
class ChatCompletionFunctionParameters(BaseModel):
    type: str = Field(
        "object",
        Literal="object",
        description="The type of the parameters, which is always 'object'.",
    )

    properties: Dict[str, ChatCompletionFunctionParametersProperty] = Field(
        ...,
        description="The properties of the parameters.",
    )

    required: List[str] = Field(
        [],
        description="The required parameters.",
    )


# This class utilizes code from the Open Source Project TaskingAI.
# The original code can be found at: https://github.com/TaskingAI/TaskingAI
class ChatCompletionFunction(BaseModel):
    name: str = Field(
        ...,
        description="The name of the function.",
        examples=["plus_a_and_b"],
    )

    description: str = Field(
        ...,
        description="The description of the function.",
        examples=["Add two numbers"],
    )

    parameters: ChatCompletionFunctionParameters = Field(
        ...,
        description="The function's parameters are represented as an object in JSON Schema format.",
        examples=[
            {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number"},
                    "b": {"type": "number", "description": "The second number"},
                },
                "required": ["a", "b"],
            }
        ],
    )


# This class utilizes code from the Open Source Project TaskingAI.
# The original code can be found at: https://github.com/TaskingAI/TaskingAI
class ActionRunRequest(BaseModel):
    parameters: Optional[Dict[str, Any]] = Field(None)
    headers: Optional[Dict[str, Any]] = Field(None)
