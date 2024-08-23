from typing import Optional, Union, List

from pydantic import Field as PDField

from sqlalchemy import Column, Enum
from sqlmodel import Field, JSON

from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin


class MessageBase(BaseModel):
    role: str = Field(sa_column=Column(Enum("assistant", "user", "system", "function", "tool"), nullable=False))
    thread_id: str = Field(nullable=False)
    object: str = Field(nullable=False, default="thread.message")
    content: Optional[list] = Field(default=None, sa_column=Column(JSON))
    file_ids: Optional[list] = Field(default=None, sa_column=Column(JSON))
    attachments: Optional[list] = Field(default=None, sa_column=Column(JSON))  # 附件
    metadata_: Optional[dict] = Field(default=None, sa_column=Column("metadata", JSON), schema_extra={"validation_alias": "metadata"})
    assistant_id: Optional[str] = Field(default=None)
    run_id: Optional[str] = Field(default=None)


class Message(MessageBase, TimeStampMixin, PrimaryKeyMixin, table=True):
    pass


class MessageCreate(BaseModel):
    role: str = Field(sa_column=Column(Enum("assistant", "user"), nullable=False))
    content: Union[str, List[dict]] = Field(nullable=False)
    file_ids: Optional[list] = Field(default=None)
    attachments: Optional[list] = Field(default=None, sa_column=Column(JSON))  # 附件
    metadata_: Optional[dict] = Field(default=None, schema_extra={"validation_alias": "metadata"})


class MessageUpdate(BaseModel):
    content: Optional[str] = Field(default=None)
    metadata_: Optional[dict] = Field(default=None, schema_extra={"validation_alias": "metadata"})


class MessageRead(MessageBase, TimeStampMixin, PrimaryKeyMixin):
    metadata_: Optional[dict] = PDField(default=None, alias="metadata")
