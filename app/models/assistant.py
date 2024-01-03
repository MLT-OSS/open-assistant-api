from typing import Optional

from sqlalchemy import Column
from sqlmodel import Field, JSON

from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin


class Assistant(BaseModel, PrimaryKeyMixin, TimeStampMixin, table=True):
    model: str = Field(nullable=False)
    object: str = Field(nullable=False, default="assistant")
    description: Optional[str] = Field(default=None)
    file_ids: Optional[list] = Field(default=None, sa_column=Column(JSON))
    instructions: Optional[str] = Field(default=None)
    metadata_: Optional[dict] = Field(default=None, sa_column=Column("metadata", JSON))
    name: Optional[str] = Field(default=None)
    tools: Optional[list] = Field(default=None, sa_column=Column(JSON))


class AssistantCreate(Assistant):
    pass


class AssistantUpdate(BaseModel, PrimaryKeyMixin, TimeStampMixin):
    model: str = Field(nullable=False)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    instructions: Optional[str] = Field(default=None)
    tools: Optional[list] = Field(default=None, sa_column=Column(JSON))
    file_ids: Optional[list] = Field(default=None, sa_column=Column(JSON))
    metadata_: Optional[dict] = Field(default=None, sa_column=Column("metadata", JSON))
