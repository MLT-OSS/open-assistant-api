from sqlmodel import Session, select

from app.exceptions.exception import ResourceNotFoundError, BadRequestError
from app.models.message import MessageCreate
from app.models.thread import Thread, ThreadUpdate, ThreadCreate
from app.models.token_relation import RelationType
from app.providers.auth_provider import auth_policy
from app.schemas.common import DeleteResponse


class ThreadService:
    @staticmethod
    def create_thread(*, session: Session, body: ThreadCreate, token_id=None) -> Thread:
        db_thread = Thread.model_validate(body)
        session.add(db_thread)
        auth_policy.insert_token_rel(
            session=session, token_id=token_id, relation_type=RelationType.Thread, relation_id=db_thread.id
        )
        session.commit()
        thread_id = db_thread.id
        # save messages
        if body.messages is not None and len(body.messages) > 0:
            from app.services.message.message import MessageService

            for message in body.messages:
                if message.role != "user":
                    raise BadRequestError(message='Role must be "user"')
                MessageService.create_message(
                    session=session,
                    thread_id=thread_id,
                    body=MessageCreate.from_orm(message),
                )
        elif body.thread_id:
            # copy thread
            from app.services.message.message import MessageService

            MessageService.copy_messages(session=session,
                                         from_thread_id=body.thread_id,
                                         to_thread_id=thread_id,
                                         end_message_id=body.end_message_id)
        session.refresh(db_thread)
        return db_thread

    @staticmethod
    def modify_thread(*, session: Session, thread_id: str, body: ThreadUpdate) -> Thread:
        db_thread = ThreadService.get_thread(session=session, thread_id=thread_id)
        update_data = body.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_thread, key, value)
        session.add(db_thread)
        session.commit()
        session.refresh(db_thread)
        return db_thread

    @staticmethod
    def delete_assistant(*, session: Session, thread_id: str) -> DeleteResponse:
        db_thread = ThreadService.get_thread(session=session, thread_id=thread_id)
        session.delete(db_thread)
        auth_policy.delete_token_rel(session=session, relation_type=RelationType.Thread, relation_id=thread_id)
        session.commit()
        return DeleteResponse(id=thread_id, object="thread.deleted", deleted=True)

    @staticmethod
    def get_thread(*, session: Session, thread_id: str) -> Thread:
        statement = select(Thread).where(Thread.id == thread_id)
        thread = session.exec(statement).one_or_none()
        if thread is None:
            raise ResourceNotFoundError(message=f"thread {thread_id} not found")
        return session.exec(statement).one_or_none()
