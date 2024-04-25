from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlmodel import select

from app.exceptions.exception import ResourceNotFoundError
from app.models import MessageFile
from app.models.message import Message, MessageCreate, MessageUpdate
from app.services.thread.thread import ThreadService


class MessageService:
    @staticmethod
    def new_message(*, session: Session, content, role, assistant_id, thread_id, run_id) -> Message:
        message = Message(
            content=[{"type": "text", "text": {"value": content, "annotations": []}}],
            role=role,
            assistant_id=assistant_id,
            thread_id=thread_id,
            run_id=run_id,
        )

        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def get_message_list(*, session: Session, thread_id) -> List[Message]:
        statement = select(Message).where(Message.thread_id == thread_id).order_by(Message.created_at)
        return session.execute(statement).scalars().all()

    @staticmethod
    async def create_message(*, session: AsyncSession, body: MessageCreate, thread_id: Optional[str] = None) -> Message:
        # get thread
        if thread_id is not None:
            await ThreadService.get_thread(thread_id=thread_id, session=session)
        # TODO message annotations
        content = [{"type": "text", "text": {"value": body.content, "annotations": []}}]
        db_message = Message.model_validate(body, update={"thread_id": thread_id, "content": content})
        session.add(db_message)
        await session.commit()
        await session.refresh(db_message)
        return db_message

    @staticmethod
    def get_message_sync(*, session: Session, thread_id: str, message_id: str) -> Message:
        statement = select(Message).where(Message.thread_id == thread_id).where(Message.id == message_id)
        result = session.execute(statement)
        message = result.scalars().one_or_none()
        if message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        return message

    @staticmethod
    def modify_message_sync(*, session: Session, thread_id: str, message_id: str, body: MessageUpdate) -> Message:
        if body.content:
            body.content = [{"type": "text", "text": {"value": body.content, "annotations": []}}]
        # get thread
        ThreadService.get_thread_sync(thread_id=thread_id, session=session)
        # get message
        db_message = MessageService.get_message_sync(session=session, thread_id=thread_id, message_id=message_id)
        update_data = body.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_message, key, value)
        session.add(db_message)
        session.commit()
        session.refresh(db_message)
        return db_message

    @staticmethod
    async def modify_message(*, session: AsyncSession, thread_id: str, message_id: str, body: MessageUpdate) -> Message:
        if body.content:
            body.content = [{"type": "text", "text": {"value": body.content, "annotations": []}}]
        # get thread
        await ThreadService.get_thread(thread_id=thread_id, session=session)
        # get message
        db_message = await MessageService.get_message(session=session, thread_id=thread_id, message_id=message_id)
        update_data = body.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_message, key, value)
        session.add(db_message)
        await session.commit()
        await session.refresh(db_message)
        return db_message

    @staticmethod
    async def get_message(*, session: AsyncSession, thread_id: str, message_id: str) -> Message:
        statement = select(Message).where(Message.thread_id == thread_id).where(Message.id == message_id)
        result = await session.execute(statement)
        message = result.scalars().one_or_none()
        if message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        return message

    @staticmethod
    async def get_message_file(*, session: AsyncSession, thread_id: str, message_id: str, file_id: str) -> MessageFile:
        await MessageService.get_message(session=session, thread_id=thread_id, message_id=message_id)
        # get message files
        statement = select(MessageFile).where(MessageFile.id == file_id).where(MessageFile.message_id == message_id)
        result = await session.execute(statement)
        msg_file = result.scalars().one_or_none()
        if msg_file is None:
            raise ResourceNotFoundError(message="Message file not found")
        return msg_file

    @staticmethod
    async def copy_messages(*, session: AsyncSession, from_thread_id: str, to_thread_id: str, end_message_id: str):
        """
        copy thread messages to another thread
        """
        statement = select(Message).where(Message.thread_id == from_thread_id)
        if end_message_id:
            statement = statement.where(Message.id <= end_message_id)
        result = await session.execute(statement.order_by(Message.id))
        original_messages = result.scalars().all()

        for original_message in original_messages:
            new_message = Message(
                thread_id=to_thread_id,
                **original_message.model_dump(exclude={"id", "created_at", "updated_at", "thread_id"}),
            )
            session.add(new_message)
        await session.commit()

    @staticmethod
    async def create_messages(*, session: AsyncSession, thread_id: str, run_id: str, assistant_id: str, messages: list):
        for original_message in messages:
            content = [
                {
                    "type": "text",
                    "text": {"value": original_message["content"], "annotations": []},
                }
            ]

            new_message = Message.model_validate(
                original_message,
                update={
                    "thread_id": thread_id,
                    "run_id": run_id,
                    "assistant_id": assistant_id,
                    "content": content,
                    "role": original_message["role"],
                },
            )
            session.add(new_message)
