from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.api.deps import get_session
from app.models.assistant_file import AssistantFileCreate, AssistantFile
from app.libs.paginate import cursor_page, CommonPage
from app.schemas.common import DeleteResponse
from app.services.assistant.assistant_file import AssistantFileService

router = APIRouter()


@router.get("/{assistant_id}/files", response_model=CommonPage[AssistantFile])
def list_assistant_files(
    *,
    session: Session = Depends(get_session),
    assistant_id: str,
):
    """
    Returns a list of assistant files.
    """
    return cursor_page(select(AssistantFile).where(AssistantFile.assistant_id == assistant_id), db=session)


@router.post("/{assistant_id}/files", response_model=AssistantFile)
def create_assistant_file(
    *,
    session: Session = Depends(get_session),
    assistant_id: str,
    body: AssistantFileCreate,
) -> AssistantFile:
    """
    Create an assistant file by attaching a [File](/docs/api-reference/files)
    to an [assistant](/docs/api-reference/assistants).
    """
    return AssistantFileService.create_assistant_file(session=session, assistant_id=assistant_id, body=body)


@router.get("/{assistant_id}/files/{file_id}", response_model=AssistantFile)
def get_assistant_file(*, session: Session = Depends(get_session), assistant_id: str, file_id: str) -> AssistantFile:
    """
    Retrieves an AssistantFile.
    """
    return AssistantFileService.get_assistant_file(session=session, assistant_id=assistant_id, file_id=file_id)


@router.delete(
    "/{assistant_id}/files/{file_id}",
    response_model=DeleteResponse,
)
def delete_assistant_file(
    *, session: Session = Depends(get_session), assistant_id: str, file_id: str
) -> DeleteResponse:
    """
    Delete an assistant file.
    """
    return AssistantFileService.delete_assistant_file(session=session, assistant_id=assistant_id, file_id=file_id)
