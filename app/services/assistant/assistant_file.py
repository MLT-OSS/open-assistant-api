from sqlmodel import Session, select

from app.exceptions.exception import ResourceNotFoundError
from app.models.assistant_file import (
    AssistantFile,
    AssistantFileCreate,
    AssistantFileUpdate,
)
from app.schemas.common import DeleteResponse


class AssistantFileService:
    @staticmethod
    def create_assistant_file(*, session: Session, assistant_id: str, body: AssistantFileCreate) -> AssistantFile:
        # TODO 关系表暂时不实现
        return AssistantFile(id="", assistant_id=assistant_id)

    @staticmethod
    def modify_assistant_file(*, session: Session, assistant_id: str, body: AssistantFileUpdate) -> AssistantFile:
        db_assistant = AssistantFileService.get_assistant_file(
            session=session, assistant_id=assistant_id, file_id=body.id
        )
        update_data = body.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_assistant, key, value)
        session.add(db_assistant)
        session.commit()
        session.refresh(db_assistant)
        return db_assistant

    @staticmethod
    def delete_assistant_file(*, session: Session, assistant_id: str, file_id: str) -> DeleteResponse:
        db_ass = AssistantFileService.get_assistant_file(session=session, assistant_id=assistant_id, file_id=file_id)
        session.delete(db_ass)
        session.commit()
        return DeleteResponse(id=assistant_id, object="assistant.deleted", deleted=True)

    @staticmethod
    def get_assistant_file(*, session: Session, assistant_id: str, file_id: str) -> AssistantFile:
        statement = select(AssistantFile).where(AssistantFile.id == assistant_id).where(AssistantFile.id == file_id)
        assistant = session.exec(statement).one_or_none()
        if assistant is None:
            raise ResourceNotFoundError(message=f"Assistant file-{file_id} not found")
        return session.exec(statement).one_or_none()
