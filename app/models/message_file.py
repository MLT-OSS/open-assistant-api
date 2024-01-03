from sqlmodel import Field

from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin


class MessageFile(BaseModel, PrimaryKeyMixin, TimeStampMixin, table=True):
    message_id: str = Field(nullable=False)
    object: str = Field(nullable=False, default="thread.message.file")
