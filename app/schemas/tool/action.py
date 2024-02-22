from typing import Optional, Any, Dict, List
from fastapi import HTTPException
from pydantic import BaseModel, Field, root_validator
from app.schemas.tool.authentication import Authentication, AuthenticationType
import openapi_spec_validator
import re
from enum import Enum


def validate_openapi_schema(schema: Dict, only_one_path_and_method: bool):
    try:
        openapi_spec_validator.validate(schema)
        # check exactly one server in the schema
    except Exception as e:
        if hasattr(e, "message"):
            raise HTTPException(
                status_code=400,
                detail={"error_code": "REQUEST_VALIDATION_ERROR", "message": f"Invalid openapi schema: {e.message}"},
            )
        else:
            raise HTTPException(
                status_code=400,
                detail={"error_code": "REQUEST_VALIDATION_ERROR", "message": f"Invalid openapi schema: {e}"},
            )
    if "servers" not in schema:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "REQUEST_VALIDATION_ERROR", "message": "No server is found in action schema"},
        )

    if "paths" not in schema:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "REQUEST_VALIDATION_ERROR", "message": "No paths is found in action schema"},
        )
    if len(schema["servers"]) != 1:
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "REQUEST_VALIDATION_ERROR",
                "message": "Exactly one server is allowed in action schema",
            },
        )

    if only_one_path_and_method:
        if len(schema["paths"]) != 1:
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": "REQUEST_VALIDATION_ERROR",
                    "message": "Only one path is allowed in action schema",
                },
            )
        path = list(schema["paths"].keys())[0]
        if len(schema["paths"][path]) != 1:
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": "REQUEST_VALIDATION_ERROR",
                    "message": "Only one method is allowed in action schema",
                },
            )

    # check each path method has a valid description and operationId
    for path, methods in schema["paths"].items():
        for method, details in methods.items():
            if not details.get("description") or not isinstance(details["description"], str):
                if details.get("summary") and isinstance(details["summary"], str):
                    # use summary as its description
                    details["description"] = details["summary"]
                else:
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "error_code": "REQUEST_VALIDATION_ERROR",
                            "message": f"No description is found in {method} {path} in action schema",
                        },
                    )

            if len(details["description"]) > 512:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error_code": "REQUEST_VALIDATION_ERROR",
                        "message": f"Description cannot be longer than 512 characters in {method} {path} in action schema",
                    },
                )

            if not details.get("operationId") or not isinstance(details["operationId"], str):
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error_code": "REQUEST_VALIDATION_ERROR",
                        "message": f"No operationId is found in {method} {path} in action schema",
                    },
                )

            if len(details["operationId"]) > 128:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error_code": "REQUEST_VALIDATION_ERROR",
                        "message": f"operationId cannot be longer than 128 characters in {method} {path} in action schema",
                    },
                )

            if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", details["operationId"]):
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error_code": "REQUEST_VALIDATION_ERROR",
                        "message": f'Invalid operationId {details["operationId"]} in {method} {path} in action schema',
                    },
                )

    return schema


# ----------------------------
# Create Action
# POST /actions


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

    @root_validator()
    def root_validator(cls, data: Any):
        openapi_schema = data.get("openapi_schema")
        validate_openapi_schema(openapi_schema, only_one_path_and_method=False)
        authentication = data.get("authentication")
        authentication.encrypt()
        return data


# ----------------------------
# Update Action
# POST /actions/{action_id}


class ActionUpdateRequest(BaseModel):
    openapi_schema: Optional[Dict] = Field(
        default=None,
        description="The action schema, which is compliant with the OpenAPI Specification. "
        "It should only have exactly one path and one method.",
    )
    authentication: Optional[Authentication] = Field(None, description="The action API authentication.")

    @root_validator()
    def root_validator(cls, data: Any):
        if not any([(data.get(key) is not None) for key in ["openapi_schema", "authentication"]]):
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": "REQUEST_VALIDATION_ERROR",
                    "message": "At least one field should be filled",
                },
            )
        openapi_schema = data.get("openapi_schema")
        validate_openapi_schema(openapi_schema, only_one_path_and_method=False)
        authentication = data.get("authentication")
        if authentication:
            authentication.encrypt()
        return data


# ----------------------------
# Run an Action
# POST /actions/{action_id}/run


class ActionRunRequest(BaseModel):
    parameters: Optional[Dict[str, Any]] = Field(None)
    headers: Optional[Dict[str, Any]] = Field(None)


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


class ActionParam(BaseModel):
    type: str
    description: str
    enum: Optional[List[str]] = None
    required: bool

    def is_single_value_enum(self):
        return self.enum and len(self.enum) == 1


class ActionBodyType(str, Enum):
    JSON = "JSON"
    FORM = "FORM"
    NONE = "NONE"


class ChatCompletionFunctionParametersProperty(BaseModel):
    type: str = Field(
        ...,
        pattern="^(string|number|integer|boolean)$",
        description="The type of the parameter.",
    )

    description: str = Field(
        "",
        max_length=256,
        description="The description of the parameter.",
    )

    enum: Optional[List[str]] = Field(
        None,
        description="The enum list of the parameter. Which is only allowed when type is 'string'.",
    )


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


class ActionRunRequest(BaseModel):
    parameters: Optional[Dict[str, Any]] = Field(None)
    headers: Optional[Dict[str, Any]] = Field(None)
