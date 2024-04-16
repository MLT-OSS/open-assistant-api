from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.deps import get_async_session, get_token_id
from app.libs.paginate import cursor_page, CommonPage
from app.models.action import Action
from app.models.token_relation import RelationType
from app.providers.auth_provider import auth_policy
from app.schemas.common import DeleteResponse, BaseSuccessDataResponse
from app.schemas.tool.action import ActionBulkCreateRequest, ActionUpdateRequest, ActionRunRequest
from app.services.tool.action import ActionService

router = APIRouter()


@router.get("", response_model=CommonPage[Action])
async def list_actions(*, session: AsyncSession = Depends(get_async_session), token_id=Depends(get_token_id)):
    """
    Returns a list of Actions.
    """
    statement = auth_policy.token_filter(
        select(Action), field=Action.id, relation_type=RelationType.Action, token_id=token_id
    )
    return await cursor_page(statement, session)


@router.post("", response_model=List[Action])
async def create_actions(
    *, session: AsyncSession = Depends(get_async_session), body: ActionBulkCreateRequest, token_id=Depends(get_token_id)
) -> List[Action]:
    """
    Create an action with openapi schema.
    """

    return await ActionService.create_actions(session=session, body=body, token_id=token_id)


@router.get("/{action_id}", response_model=Action)
async def get_action(*, session: AsyncSession = Depends(get_async_session), action_id: str) -> Action:
    """
    Retrieves an action.
    """
    return await ActionService.get_action(session=session, action_id=action_id)


@router.post("/{action_id}", response_model=Action)
async def modify_action(
    *, session: AsyncSession = Depends(get_async_session), action_id: str, body: ActionUpdateRequest
) -> Action:
    """
    Modifies an action.
    """
    return await ActionService.modify_action(session=session, action_id=action_id, body=body)


@router.delete("/{action_id}", response_model=DeleteResponse)
async def delete_action(*, session: AsyncSession = Depends(get_async_session), action_id: str) -> DeleteResponse:
    """
    Delete an action.
    """
    return await ActionService.delete_action(session=session, action_id=action_id)


@router.post(
    "/{action_id}/run",
    response_model=BaseSuccessDataResponse,
)
async def api_run_action(*, session: AsyncSession = Depends(get_async_session), action_id: str, body: ActionRunRequest):
    response: Dict = await ActionService.run_action(
        session=session,
        action_id=action_id,
        parameters=body.parameters,
        headers=body.headers,
    )
    return BaseSuccessDataResponse(data=response)
