from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.deps import get_async_session
from app.models import MessageFile
from app.models.message import Message, MessageCreate, MessageUpdate
from app.libs.paginate import cursor_page, CommonPage
from app.services.message.message import MessageService

router = APIRouter()


@router.get(
    "/{thread_id}/messages",
    response_model=CommonPage[Message],
)
async def list_messages(
    *,
    session: AsyncSession = Depends(get_async_session),
    thread_id: str,
):
    """
    Returns a list of messages for a given thread.
    """
    return await cursor_page(select(Message).where(Message.thread_id == thread_id), session)


@router.post("/{thread_id}/messages", response_model=Message)
async def create_message(
    *, session: AsyncSession = Depends(get_async_session), thread_id: str, body: MessageCreate
) -> Message:
    """
    Create a message.
    """
    return await MessageService.create_message(session=session, thread_id=thread_id, body=body)


@router.get(
    "/{thread_id}/messages/{message_id}",
    response_model=Message,
)
async def get_message(
    *, session: AsyncSession = Depends(get_async_session), thread_id: str, message_id: str
) -> Message:
    """
    Retrieve a message.
    """
    return await MessageService.get_message(session=session, thread_id=thread_id, message_id=message_id)


@router.post(
    "/{thread_id}/messages/{message_id}",
    response_model=Message,
)
async def modify_message(
    *,
    session: AsyncSession = Depends(get_async_session),
    thread_id: str,
    message_id: str = ...,
    body: MessageUpdate = ...,
) -> Message:
    """
    Modifies a message.
    """
    return await MessageService.modify_message(session=session, thread_id=thread_id, message_id=message_id, body=body)


@router.get(
    "/{thread_id}/messages/{message_id}/files",
    response_model=CommonPage[MessageFile],
)
async def list_message_files(
    *,
    session: AsyncSession = Depends(get_async_session),
    message_id: str = ...,
):
    """
    Returns a list of message files.
    """
    return await cursor_page(select(MessageFile).where(MessageFile.message_id == message_id), session)


@router.get(
    "/{thread_id}/messages/{message_id}/files/{file_id}",
    response_model=MessageFile,
)
async def get_message_file(
    *,
    session: AsyncSession = Depends(get_async_session),
    thread_id: str,
    message_id: str = ...,
    file_id: str = ...,
) -> MessageFile:
    """
    Retrieves a message file.
    """
    return await MessageService.get_message_file(
        session=session, thread_id=thread_id, message_id=message_id, file_id=file_id
    )
