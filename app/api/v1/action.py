from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.api.deps import get_session
from app.models.action import Action
from app.schemas.tool.action import ActionBulkCreateRequest, ActionUpdateRequest, ActionRunRequest
from app.libs.paginate import cursor_page, CommonPage
from app.schemas.common import DeleteResponse, BaseSuccessDataResponse
from app.services.tool.action import ActionService
from typing import Dict, List


router = APIRouter()


@router.get("", response_model=CommonPage[Action])
def list_actions(*, session: Session = Depends(get_session)):
    """
    Returns a list of Actions.
    """
    return cursor_page(select(Action), session)


@router.post("", response_model=List[Action])
def create_actions(*, session: Session = Depends(get_session), body: ActionBulkCreateRequest) -> Action:
    """
    Create an action with openapi schema.
    """

    return ActionService.create_actions(session=session, body=body)


@router.get("/{action_id}", response_model=Action)
def get_action(*, session: Session = Depends(get_session), action_id: str) -> Action:
    """
    Retrieves an action.
    """
    return ActionService.get_action(session=session, action_id=action_id)


@router.post("/{action_id}", response_model=Action)
def modify_action(*, session: Session = Depends(get_session), action_id: str, body: ActionUpdateRequest) -> Action:
    """
    Modifies an action.
    """
    return ActionService.modify_action(session=session, action_id=action_id, body=body)


@router.delete("/{action_id}", response_model=DeleteResponse)
def delete_action(*, session: Session = Depends(get_session), action_id: str) -> DeleteResponse:
    """
    Delete an action.
    """
    return ActionService.delete_action(session=session, action_id=action_id)


@router.post(
    "/{action_id}/run",
    response_model=BaseSuccessDataResponse,
)
def api_run_action(*, session: Session = Depends(get_session), action_id: str, body: ActionRunRequest):
    response: Dict = ActionService.run_action(
        session=session,
        action_id=action_id,
        parameters=body.parameters,
        headers=body.headers,
    )
    return BaseSuccessDataResponse(data=response)
