from typing import Optional

from sqlalchemy import Column
from sqlmodel import Field, JSON, TEXT

from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin


class AssistantBase(BaseModel):
    model: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    file_ids: Optional[list] = Field(default=None, sa_column=Column(JSON))
    instructions: Optional[str] = Field(default=None, max_length=32768, sa_column=Column(TEXT))
    metadata_: Optional[dict] = Field(default=None, sa_column=Column("metadata", JSON))
    name: Optional[str] = Field(default=None)
    tools: Optional[list] = Field(default=None, sa_column=Column(JSON))
    extra_body: Optional[dict] = Field(default=None, sa_column=Column(JSON))


class Assistant(AssistantBase, PrimaryKeyMixin, TimeStampMixin, table=True):
    object: str = Field(nullable=False, default="assistant")


class AssistantCreate(AssistantBase):
    pass


class AssistantUpdate(AssistantBase):
    pass
