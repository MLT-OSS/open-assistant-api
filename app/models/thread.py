from typing import Optional

from sqlalchemy import Column
from sqlmodel import Field, JSON

from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin
from app.models.message import MessageCreate


class Thread(BaseModel, PrimaryKeyMixin, TimeStampMixin, table=True):
    object: str = Field(nullable=False, default="thread")
    metadata_: Optional[dict] = Field(default=None, sa_column=Column("metadata", JSON), schema_extra={"validation_alias": "metadata"})
    tool_resources: Optional[dict] = Field(default=None, sa_column=Column(JSON))  # 工具资源


class ThreadCreate(BaseModel):
    object: str = "thread"
    messages: Optional[list[MessageCreate]] = Field(default=None)
    metadata_: Optional[dict] = Field(default=None, schema_extra={"validation_alias": "metadata"})
    thread_id: Optional[str] = Field(default=None)
    end_message_id: Optional[str] = Field(default=None)
    tool_resources: Optional[dict] = Field(default=None, sa_column=Column(JSON))  # 工具资源


class ThreadUpdate(BaseModel):
    metadata_: Optional[dict] = Field(default=None, schema_extra={"validation_alias": "metadata"})
