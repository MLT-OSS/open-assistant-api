from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.deps import get_session, get_token_id
from app.models.thread import Thread, ThreadUpdate, ThreadCreate
from app.schemas.common import DeleteResponse
from app.services.thread.thread import ThreadService

router = APIRouter()


@router.post("", response_model=Thread)
def create_thread(
    *, session: Session = Depends(get_session), body: ThreadCreate, token_id=Depends(get_token_id)
) -> Thread:
    """
    Create a thread.
    """
    return ThreadService.create_thread(session=session, body=body, token_id=token_id)


@router.get("/{thread_id}", response_model=Thread)
def get_thread(*, session: Session = Depends(get_session), thread_id: str) -> Thread:
    """
    Retrieves a thread.
    """
    return ThreadService.get_thread(session=session, thread_id=thread_id)


@router.post("/{thread_id}", response_model=Thread)
def modify_thread(*, session: Session = Depends(get_session), thread_id: str, body: ThreadUpdate) -> Thread:
    """
    Modifies a thread.
    """
    return ThreadService.modify_thread(session=session, thread_id=thread_id, body=body)


@router.delete("/{thread_id}", response_model=DeleteResponse)
def delete_thread(*, session: Session = Depends(get_session), thread_id: str) -> DeleteResponse:
    """
    Delete a thread.
    """
    return ThreadService.delete_assistant(session=session, thread_id=thread_id)
