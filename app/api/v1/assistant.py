from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.api.deps import get_session
from app.models.assistant import Assistant, AssistantUpdate
from app.libs.paginate import cursor_page, CommonPage
from app.schemas.common import DeleteResponse
from app.services.assistant.assistant import AssistantService

router = APIRouter()


@router.get("", response_model=CommonPage[Assistant])
def list_assistants(*, session: Session = Depends(get_session)):
    """
    Returns a list of assistants.
    """
    return cursor_page(select(Assistant), session)


@router.post("", response_model=Assistant)
def create_assistant(*, session: Session = Depends(get_session), body: Assistant) -> Assistant:
    """
    Create an assistant with a model and instructions.
    """
    return AssistantService.create_assistant(session=session, body=body)


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
