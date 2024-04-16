from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.deps import get_async_session
from app.libs.paginate import cursor_page, CommonPage
from app.models.assistant_file import AssistantFileCreate, AssistantFile
from app.schemas.common import DeleteResponse
from app.services.assistant.assistant_file import AssistantFileService

router = APIRouter()


@router.get("/{assistant_id}/files", response_model=CommonPage[AssistantFile])
async def list_assistant_files(
    *,
    session: AsyncSession = Depends(get_async_session),
    assistant_id: str,
):
    """
    Returns a list of assistant files.
    """
    return await cursor_page(select(AssistantFile).where(AssistantFile.assistant_id == assistant_id), db=session)


@router.post("/{assistant_id}/files", response_model=AssistantFile)
async def create_assistant_file(
    *,
    session: AsyncSession = Depends(get_async_session),
    assistant_id: str,
    body: AssistantFileCreate,
) -> AssistantFile:
    """
    Create an assistant file by attaching a [File](/docs/api-reference/files)
    to an [assistant](/docs/api-reference/assistants).
    """
    return await AssistantFileService.create_assistant_file(session=session, assistant_id=assistant_id, body=body)


@router.get("/{assistant_id}/files/{file_id}", response_model=AssistantFile)
async def get_assistant_file(
    *, session: AsyncSession = Depends(get_async_session), assistant_id: str, file_id: str
) -> AssistantFile:
    """
    Retrieves an AssistantFile.
    """
    return await AssistantFileService.get_assistant_file(session=session, assistant_id=assistant_id, file_id=file_id)


@router.delete(
    "/{assistant_id}/files/{file_id}",
    response_model=DeleteResponse,
)
async def delete_assistant_file(
    *, session: AsyncSession = Depends(get_async_session), assistant_id: str, file_id: str
) -> DeleteResponse:
    """
    Delete an assistant file.
    """
    return await AssistantFileService.delete_assistant_file(session=session, assistant_id=assistant_id, file_id=file_id)
