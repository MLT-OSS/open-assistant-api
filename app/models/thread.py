from typing import Optional

from sqlalchemy import Column
from sqlmodel import Field, JSON

from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin
from app.models.message import MessageCreate


class Thread(BaseModel, PrimaryKeyMixin, TimeStampMixin, table=True):
    object: str = Field(nullable=False, default="thread")
    metadata_: Optional[dict] = Field(default=None, sa_column=Column("metadata", JSON))


class ThreadCreate(BaseModel):
    object: str = "thread"
    messages: Optional[list[MessageCreate]]
    # metadata: Optional[dict]


class ThreadUpdate(BaseModel):
    metadata_: Optional[dict] = Field(alias="metadata")
