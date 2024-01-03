from sqlmodel import Session, select

from app.exceptions.exception import ResourceNotFoundError
from app.models.assistant import Assistant, AssistantUpdate
from app.schemas.common import DeleteResponse


class AssistantService:
    @staticmethod
    def create_assistant(*, session: Session, body: Assistant) -> Assistant:
        session.add(body)
        session.commit()
        session.refresh(body)
        return body

    @staticmethod
    def modify_assistant(*, session: Session, assistant_id: str, body: AssistantUpdate) -> Assistant:
        db_assistant = AssistantService.get_assistant(session=session, assistant_id=assistant_id)
        update_data = body.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_assistant, key, value)
        session.add(db_assistant)
        session.commit()
        session.refresh(db_assistant)
        return db_assistant

    @staticmethod
    def delete_assistant(*, session: Session, assistant_id: str) -> DeleteResponse:
        db_ass = AssistantService.get_assistant(session=session, assistant_id=assistant_id)
        session.delete(db_ass)
        session.commit()
        return DeleteResponse(id=assistant_id, object="assistant.deleted", deleted=True)

    @staticmethod
    def get_assistant(*, session: Session, assistant_id: str) -> Assistant:
        statement = select(Assistant).where(Assistant.id == assistant_id)
        assistant = session.exec(statement).one_or_none()
        if assistant is None:
            raise ResourceNotFoundError(message="Assistant not found")
        return session.exec(statement).one_or_none()
