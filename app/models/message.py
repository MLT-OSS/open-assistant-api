from typing import Optional

from sqlalchemy import Column, Enum
from sqlmodel import Field, JSON

from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin


class Message(BaseModel, TimeStampMixin, PrimaryKeyMixin, table=True):
    role: str = Field(sa_column=Column(Enum("assistant", "user", "system", "function", "tool"), nullable=False))
    thread_id: str = Field(nullable=False)
    object: str = Field(nullable=False, default="thread.message")
    content: Optional[list] = Field(default=None, sa_column=Column(JSON))
    file_ids: Optional[list] = Field(default=None, sa_column=Column(JSON))
    metadata_: Optional[dict] = Field(default=None, sa_column=Column("metadata", JSON))
    assistant_id: Optional[str] = Field(default=None)
    run_id: Optional[str] = Field(default=None)


class MessageCreate(BaseModel):
    role: str
    content: str
    file_ids: Optional[list]
    metadata_: Optional[dict]


class MessageUpdate(BaseModel):
    # thread_id: str
    # assistant_id: Optional[str]
    content: Optional[str]
    metadata_: Optional[dict]
