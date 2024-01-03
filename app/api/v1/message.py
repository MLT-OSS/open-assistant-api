from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.api.deps import get_session
from app.models import MessageFile
from app.models.message import Message, MessageCreate, MessageUpdate
from app.libs.paginate import cursor_page, CommonPage
from app.services.message.message import MessageService

router = APIRouter()


@router.get(
    "/{thread_id}/messages",
    response_model=CommonPage[Message],
)
def list_messages(
    *,
    session: Session = Depends(get_session),
    thread_id: str,
):
    """
    Returns a list of messages for a given thread.
    """
    return cursor_page(select(Message).where(Message.thread_id == thread_id), session)


@router.post("/{thread_id}/messages", response_model=Message)
def create_message(*, session: Session = Depends(get_session), thread_id: str, body: MessageCreate) -> Message:
    """
    Create a message.
    """
    return MessageService.create_message(session=session, thread_id=thread_id, body=body)


@router.get(
    "/{thread_id}/messages/{message_id}",
    response_model=Message,
)
def get_message(*, session: Session = Depends(get_session), thread_id: str, message_id: str) -> Message:
    """
    Retrieve a message.
    """
    return MessageService.get_message(session=session, thread_id=thread_id, message_id=message_id)


@router.post(
    "/{thread_id}/messages/{message_id}",
    response_model=Message,
)
def modify_message(
    *,
    session: Session = Depends(get_session),
    thread_id: str,
    message_id: str = ...,
    body: MessageUpdate = ...,
) -> Message:
    """
    Modifies a message.
    """
    return MessageService.modify_message(session=session, thread_id=thread_id, message_id=message_id, body=body)


@router.get(
    "/{thread_id}/messages/{message_id}/files",
    response_model=CommonPage[MessageFile],
)
def list_message_files(
    *,
    session: Session = Depends(get_session),
    message_id: str = ...,
):
    """
    Returns a list of message files.
    """
    return cursor_page(select(MessageFile).where(MessageFile.message_id == message_id), session)


@router.get(
    "/{thread_id}/messages/{message_id}/files/{file_id}",
    response_model=MessageFile,
)
def get_message_file(
    *,
    session: Session = Depends(get_session),
    thread_id: str,
    message_id: str = ...,
    file_id: str = ...,
) -> MessageFile:
    """
    Retrieves a message file.
    """
    return MessageService.get_message_file(session=session, thread_id=thread_id, message_id=message_id, file_id=file_id)
