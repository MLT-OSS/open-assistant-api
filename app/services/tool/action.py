import copy
from typing import Dict, List

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exception import ResourceNotFoundError, ValidateFailedError
from app.models.action import Action
from app.models.token_relation import RelationType
from app.providers.auth_provider import auth_policy
from app.schemas.common import DeleteResponse
from app.schemas.tool.action import (
    ActionBulkCreateRequest,
    ActionUpdateRequest,
    ActionMethod,
    ActionBodyType,
)
from app.schemas.tool.authentication import Authentication
from app.services.tool.openapi_call import call_action_api
from app.services.tool.openapi_utils import (
    split_openapi_schema,
    replace_openapi_refs,
    function_name,
    extract_params,
    build_function_def,
    action_param_schema_to_dict,
    action_param_dict_to_schema,
)


class ActionService:
    @staticmethod
    async def create_actions(
        *, session: AsyncSession, body: ActionBulkCreateRequest, token_id: str = None
    ) -> List[Action]:
        openapi_schema = replace_openapi_refs(body.openapi_schema)
        schemas = split_openapi_schema(openapi_schema)
        if not schemas:
            raise ValidateFailedError("Failed to parse OpenAPI schema")

        if not body.authentication.is_encrypted():
            raise Exception("Authentication must be encrypted")
        actions = []
        for schema in schemas:
            action = ActionService.build_action_struct(schema)
            action.authentication = body.authentication.dict()
            action.use_for_everyone = body.use_for_everyone
            actions.append(action)
            auth_policy.insert_token_rel(
                session=session, token_id=token_id, relation_type=RelationType.Action, relation_id=str(action.id)
            )
        session.add_all(actions)
        await session.commit()
        for action in actions:
            await session.refresh(action)
        return actions

    @staticmethod
    def create_actions_sync(
        *, session: AsyncSession, body: ActionBulkCreateRequest, token_id: str = None
    ) -> List[Action]:
        openapi_schema = replace_openapi_refs(body.openapi_schema)
        schemas = split_openapi_schema(openapi_schema)
        if not schemas:
            raise ValidateFailedError("Failed to parse OpenAPI schema")

        if not body.authentication.is_encrypted():
            raise Exception("Authentication must be encrypted")
        actions = []
        for schema in schemas:
            action = ActionService.build_action_struct(schema)
            action.authentication = body.authentication.dict()
            action.use_for_everyone = body.use_for_everyone
            actions.append(action)
            auth_policy.insert_token_rel(
                session=session, token_id=token_id, relation_type=RelationType.Action, relation_id=str(action.id)
            )
        session.add_all(actions)
        session.commit()
        for action in actions:
            session.refresh(action)
        return actions

    @staticmethod
    async def modify_action(*, session: AsyncSession, action_id: str, body: ActionUpdateRequest) -> Action:
        db_action = await ActionService.get_action(session=session, action_id=action_id)
        update_dict = {}
        if body.openapi_schema is not None:
            openapi_schema = replace_openapi_refs(body.openapi_schema)
            action: Action = ActionService.build_action_struct(openapi_schema)
            update_dict["openapi_schema"] = action.openapi_schema
            update_dict["name"] = action.name
            update_dict["description"] = action.description
            update_dict["operation_id"] = action.operation_id
            update_dict["url"] = action.url
            update_dict["method"] = action.method
            update_dict["path_param_schema"] = action.path_param_schema
            update_dict["query_param_schema"] = action.query_param_schema
            update_dict["body_type"] = action.body_type
            update_dict["body_param_schema"] = action.body_param_schema
            update_dict["function_def"] = action.function_def

        if body.authentication is not None:
            update_dict["authentication"] = body.authentication.dict()

        if body.use_for_everyone is not None:
            update_dict["use_for_everyone"] = body.use_for_everyone

        for key, value in update_dict.items():
            setattr(db_action, key, value)
        session.add(db_action)
        await session.commit()
        await session.refresh(db_action)
        return db_action

    @staticmethod
    async def delete_action(*, session: AsyncSession, action_id: str) -> DeleteResponse:
        action = await ActionService.get_action(session=session, action_id=action_id)
        await session.delete(action)
        await auth_policy.delete_token_rel(session=session, relation_type=RelationType.Action, relation_id=action_id)
        await session.commit()
        return DeleteResponse(id=action_id, object="action.deleted", deleted=True)

    @staticmethod
    async def get_action(*, session: AsyncSession, action_id: str) -> Action:
        statement = select(Action).where(Action.id == action_id)
        result = await session.execute(statement)
        action = result.scalars().one_or_none()
        if action is None:
            raise ResourceNotFoundError(message="action not found")
        return action

    @staticmethod
    def build_action_struct(
        openapi_schema: Dict,
    ) -> Action:
        """
        Extract action components from OpenAPI schema.
        :param openapi_schema: a dict of OpenAPI schema
        :return: an Action including all the components of an action
        """

        # copy openapi_schema to avoid modifying the original
        openapi_dict = copy.deepcopy(openapi_schema)

        # extract the first path and method
        path, path_info = next(iter(openapi_dict["paths"].items()))
        method, method_info = next(iter(path_info.items()))

        # check operationId
        operation_id = method_info.get("operationId", None)

        # get function name
        name = function_name(method, path, operation_id)
        method = ActionMethod(method.upper())

        # extract description
        description = method_info.get("description", "")
        if not description:
            # use other fields to generate description
            summary = method_info.get("summary", "")
            description = f"{method.upper()} {path}: {summary}"

        # build function parameters schema
        url, path_param_schema, query_param_schema, body_type, body_param_schema = extract_params(
            openapi_dict, method, path
        )

        # build function definition
        function_def = build_function_def(
            name=name,
            description=description,
            path_param_schema=path_param_schema,
            query_param_schema=query_param_schema,
            body_param_schema=body_param_schema,
        )
        return Action.model_validate(
            {
                "name": name,
                "description": description,
                "operation_id": operation_id,
                "url": url,
                "method": method,
                "path_param_schema": action_param_schema_to_dict(path_param_schema),
                "query_param_schema": action_param_schema_to_dict(query_param_schema),
                "body_type": body_type,
                "body_param_schema": action_param_schema_to_dict(body_param_schema),
                "function_def": function_def.dict(exclude_none=True),
                "openapi_schema": openapi_dict,
            }
        )

    @staticmethod
    async def run_action(
        *,
        session: AsyncSession,
        action_id: str,
        parameters: Dict,
        headers: Dict,
    ) -> Dict:
        """
        Run an action
        :param action_id: the action ID
        :param parameters: the parameters for the API call
        :param headers: the headers for the API call
        :return: the response of the API call
        """
        action: Action = await ActionService.get_action(session=session, action_id=action_id)

        response = call_action_api(
            url=action.url,
            method=ActionMethod(action.method),
            path_param_schema=action_param_dict_to_schema(action.path_param_schema),
            query_param_schema=action_param_dict_to_schema(action.query_param_schema),
            body_param_schema=action_param_dict_to_schema(action.body_param_schema),
            body_type=ActionBodyType(action.body_type),
            parameters=parameters,
            headers=headers,
            authentication=Authentication(**action.authentication),
        )
        return response
