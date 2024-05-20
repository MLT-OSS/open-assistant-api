from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_token_id, get_async_session
from app.models.thread import Thread, ThreadUpdate, ThreadCreate
from app.schemas.common import DeleteResponse
from app.services.thread.thread import ThreadService

router = APIRouter()


@router.post("", response_model=Thread)
async def create_thread(
    *, session: AsyncSession = Depends(get_async_session), body: ThreadCreate, token_id=Depends(get_token_id)
) -> Thread:
    """
    Create a thread.
    """
    return await ThreadService.create_thread(session=session, body=body, token_id=token_id)


@router.get("/{thread_id}", response_model=Thread)
async def get_thread(*, session: AsyncSession = Depends(get_async_session), thread_id: str) -> Thread:
    """
    Retrieves a thread.
    """
    return await ThreadService.get_thread(session=session, thread_id=thread_id)


@router.post("/{thread_id}", response_model=Thread)
async def modify_thread(
    *, session: AsyncSession = Depends(get_async_session), thread_id: str, body: ThreadUpdate
) -> Thread:
    """
    Modifies a thread.
    """
    return await ThreadService.modify_thread(session=session, thread_id=thread_id, body=body)


@router.delete("/{thread_id}", response_model=DeleteResponse)
async def delete_thread(*, session: AsyncSession = Depends(get_async_session), thread_id: str) -> DeleteResponse:
    """
    Delete a thread.
    """
    return await ThreadService.delete_assistant(session=session, thread_id=thread_id)
