from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.api.deps import get_token_id, get_session
from app.models.assistant import Assistant, AssistantUpdate, AssistantCreate
from app.libs.paginate import cursor_page, CommonPage
from app.models.token_relation import RelationType
from app.providers.auth_provider import auth_policy
from app.schemas.common import DeleteResponse
from app.services.assistant.assistant import AssistantService

router = APIRouter()


@router.get("", response_model=CommonPage[Assistant])
def list_assistants(*, session: Session = Depends(get_session), token_id=Depends(get_token_id)):
    """
    Returns a list of assistants.
    """
    statement = auth_policy.token_filter(
        select(Assistant), field=Assistant.id, relation_type=RelationType.Assistant, token_id=token_id
    )
    return cursor_page(statement, session)


@router.post("", response_model=Assistant)
def create_assistant(
    *, session: Session = Depends(get_session), body: AssistantCreate, token_id=Depends(get_token_id)
) -> Assistant:
    """
    Create an assistant with a model and instructions.
    """
    return AssistantService.create_assistant(session=session, body=body, token_id=token_id)


@router.get("/{assistant_id}", response_model=Assistant)
def get_assistant(*, session: Session = Depends(get_session), assistant_id: str) -> Assistant:
    """
    Retrieves an assistant.
    """
    return AssistantService.get_assistant(session=session, assistant_id=assistant_id)


@router.post("/{assistant_id}", response_model=Assistant)
def modify_assistant(*, session: Session = Depends(get_session), assistant_id: str, body: AssistantUpdate) -> Assistant:
    """
    Modifies an assistant.
    """
    return AssistantService.modify_assistant(session=session, assistant_id=assistant_id, body=body)


@router.delete("/{assistant_id}", response_model=DeleteResponse)
def delete_assistant(*, session: Session = Depends(get_session), assistant_id: str) -> DeleteResponse:
    """
    Delete an assistant.
    """
    return AssistantService.delete_assistant(session=session, assistant_id=assistant_id)
