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
    def format_message_content(message_create: MessageCreate) -> List:
        content = []
        if isinstance(message_create.content, str):
            content.append({"type": "text", "text": {"value": message_create.content, "annotations": []}})
        elif isinstance(message_create.content, list):
            for msg in message_create.content:
                if msg.get("type") == "text":
                    msg_value = msg.get("text")
                    content.append({"type": "text", "text": {"value": msg_value, "annotations": []}})
                elif msg.get("type") == "image_file" or msg.get("type") == "image_url":
                    content.append(msg)
        return content

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
    async def create_message(*, session: AsyncSession, body: MessageCreate, thread_id: str) -> Message:
        # get thread
        thread = await ThreadService.get_thread(thread_id=thread_id, session=session)
        # TODO message annotations
        body_file_ids = body.file_ids
        if body.attachments:
            body_file_ids = [a.get("file_id") for a in body.attachments]

        if body_file_ids:
            thread_file_ids = []
            if thread.tool_resources and "file_search" in thread.tool_resources:
                thread_file_ids = thread.tool_resources.get("file_search").get("vector_stores")[0].get("file_ids")
            for file_id in body_file_ids:
                if file_id not in thread_file_ids:
                    thread_file_ids.append(file_id)

            if thread_file_ids:
                if not thread.tool_resources:
                    thread.tool_resources = {}
                if "file_search" not in thread.tool_resources:
                    thread.tool_resources["file_search"] = {"vector_stores": [{"file_ids": []}]}
                thread.tool_resources.get("file_search").get("vector_stores")[0]["file_ids"] = thread_file_ids
                session.add(thread)

        content = MessageService.format_message_content(body)
        db_message = Message.model_validate(body.model_dump(by_alias=True), update={"thread_id": thread_id, "content": content}, from_attributes=True)
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
            content = MessageService.format_message_content(original_message)
            new_message = Message.model_validate(
                original_message.model_dump(by_alias=True),
                update={
                    "thread_id": thread_id,
                    "run_id": run_id,
                    "assistant_id": assistant_id,
                    "content": content,
                    "role": original_message.role,
                },
            )
            session.add(new_message)
