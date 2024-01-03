from sqlalchemy import Index
from sqlmodel import Field

from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin


class AssistantFileBase(BaseModel):
    __table_args__ = (Index("assistant_file_assistant_id_id_idx", "assistant_id", "id"),)

    assistant_id: str = Field(nullable=False)
    object: str = Field(nullable=False, default="assistant.file")


class AssistantFile(AssistantFileBase, PrimaryKeyMixin, TimeStampMixin, table=True):
    pass


class AssistantFileCreate(AssistantFileBase):
    pass


class AssistantFileUpdate(BaseModel, PrimaryKeyMixin, TimeStampMixin):
    pass
