from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.exceptions.exception import ResourceNotFoundError, BadRequestError
from app.models.message import MessageCreate
from app.models.thread import Thread, ThreadUpdate, ThreadCreate
from app.models.token_relation import RelationType
from app.providers.auth_provider import auth_policy
from app.schemas.common import DeleteResponse


class ThreadService:
    @staticmethod
    async def create_thread(*, session: AsyncSession, body: ThreadCreate, token_id=None) -> Thread:
        db_thread = Thread.model_validate(body.model_dump(by_alias=True))
        session.add(db_thread)
        auth_policy.insert_token_rel(
            session=session, token_id=token_id, relation_type=RelationType.Thread, relation_id=db_thread.id
        )
        await session.commit()
        await session.refresh(db_thread)
        thread_id = db_thread.id
        # save messages
        if body.messages is not None and len(body.messages) > 0:
            from app.services.message.message import MessageService

            for message in body.messages:
                if message.role != "user" and message.role != "assistant":
                    raise BadRequestError(message='Role must be "user" or "assistant"')
                await MessageService.create_message(
                    session=session,
                    thread_id=thread_id,
                    body=MessageCreate.model_validate(message.model_dump(by_alias=True)),
                )
        elif body.thread_id:
            # copy thread
            from app.services.message.message import MessageService

            await MessageService.copy_messages(
                session=session,
                from_thread_id=body.thread_id,
                to_thread_id=thread_id,
                end_message_id=body.end_message_id,
            )
        await session.refresh(db_thread)
        return db_thread

    @staticmethod
    async def modify_thread(*, session: AsyncSession, thread_id: str, body: ThreadUpdate) -> Thread:
        db_thread = await ThreadService.get_thread(session=session, thread_id=thread_id)
        update_data = body.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_thread, key, value)
        session.add(db_thread)
        await session.commit()
        await session.refresh(db_thread)
        return db_thread

    @staticmethod
    async def delete_assistant(*, session: AsyncSession, thread_id: str) -> DeleteResponse:
        db_thread = await ThreadService.get_thread(session=session, thread_id=thread_id)
        await session.delete(db_thread)
        await auth_policy.delete_token_rel(session=session, relation_type=RelationType.Thread, relation_id=thread_id)
        await session.commit()
        return DeleteResponse(id=thread_id, object="thread.deleted", deleted=True)

    @staticmethod
    async def get_thread(*, session: AsyncSession, thread_id: str) -> Thread:
        statement = select(Thread).where(Thread.id == thread_id)
        result = await session.execute(statement)
        thread = result.scalars().one_or_none()
        if thread is None:
            raise ResourceNotFoundError(message=f"thread {thread_id} not found")
        return thread

    @staticmethod
    def get_thread_sync(*, session: Session, thread_id: str) -> Thread:
        statement = select(Thread).where(Thread.id == thread_id)
        result = session.execute(statement)
        thread = result.scalars().one_or_none()
        if thread is None:
            raise ResourceNotFoundError(message=f"thread {thread_id} not found")
        return thread
