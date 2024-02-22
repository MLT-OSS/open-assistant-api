from sqlmodel import Session, select

from app.exceptions.exception import ResourceNotFoundError
from app.models.assistant import Assistant, AssistantUpdate, AssistantCreate
from app.models.token_relation import RelationType
from app.providers.auth_provider import auth_policy
from app.schemas.common import DeleteResponse


class AssistantService:
    @staticmethod
    def create_assistant(*, session: Session, body: AssistantCreate, token_id: str = None) -> Assistant:
        db_assistant = Assistant.model_validate(body)
        session.add(db_assistant)
        auth_policy.insert_token_rel(
            session=session, token_id=token_id, relation_type=RelationType.Assistant, relation_id=db_assistant.id
        )
        session.commit()
        session.refresh(db_assistant)
        return db_assistant

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
    def delete_assistant(
        *,
        session: Session,
        assistant_id: str,
    ) -> DeleteResponse:
        db_ass = AssistantService.get_assistant(session=session, assistant_id=assistant_id)
        session.delete(db_ass)
        auth_policy.delete_token_rel(session=session, relation_type=RelationType.Assistant, relation_id=assistant_id)
        session.commit()
        return DeleteResponse(id=assistant_id, object="assistant.deleted", deleted=True)

    @staticmethod
    def get_assistant(*, session: Session, assistant_id: str) -> Assistant:
        statement = select(Assistant).where(Assistant.id == assistant_id)
        assistant = session.exec(statement).one_or_none()
        if assistant is None:
            raise ResourceNotFoundError(message="Assistant not found")
        return session.exec(statement).one_or_none()
