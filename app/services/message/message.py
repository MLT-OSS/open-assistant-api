from typing import List, Optional

from fastapi import HTTPException
from sqlmodel import Session, select

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
        return session.exec(statement).all()

    @staticmethod
    def create_message(*, session: Session, body: MessageCreate, thread_id: Optional[str] = None) -> Message:
        # get thread
        if thread_id is not None:
            ThreadService.get_thread(thread_id=thread_id, session=session)
        # TODO message annotations
        content = [{"type": "text", "text": {"value": body.content, "annotations": []}}]
        db_message = Message.model_validate(body, update={"thread_id": thread_id, "content": content})
        session.add(db_message)
        session.commit()
        session.refresh(db_message)
        return db_message

    @staticmethod
    def modify_message(*, session: Session, thread_id: str, message_id: str, body: MessageUpdate) -> Message:
        # get thread
        ThreadService.get_thread(thread_id=thread_id, session=session)
        # get message
        db_message = MessageService.get_message(session=session, thread_id=thread_id, message_id=message_id)
        update_data = body.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_message, key, value)
        session.add(db_message)
        session.commit()
        session.refresh(db_message)
        return db_message

    @staticmethod
    def get_message(*, session: Session, thread_id: str, message_id: str) -> Message:
        statement = select(Message).where(Message.thread_id == thread_id).where(Message.id == message_id)
        assistant = session.exec(statement).one_or_none()
        if assistant is None:
            raise HTTPException(status_code=404, detail="Message not found")
        return session.exec(statement).one_or_none()

    @staticmethod
    def get_message_file(*, session: Session, thread_id: str, message_id: str, file_id: str) -> MessageFile:
        MessageService.get_message(session=session, thread_id=thread_id, message_id=message_id)
        # get message files
        statement = select(MessageFile).where(MessageFile.id == file_id).where(MessageFile.message_id == message_id)
        msg_file = session.exec(statement).one_or_none()
        if msg_file is None:
            raise ResourceNotFoundError(message="Message file not found")
        return msg_file
