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
    response_format: Optional[str] = Field(default=None)  # 响应格式
    tool_resources: Optional[dict] = Field(default=None, sa_column=Column(JSON))  # 工具资源
    temperature: Optional[float] = Field(default=None)  # 温度
    top_p: Optional[float] = Field(default=None)  # top_p


class Assistant(AssistantBase, PrimaryKeyMixin, TimeStampMixin, table=True):
    object: str = Field(nullable=False, default="assistant")


class AssistantCreate(AssistantBase):
    pass


class AssistantUpdate(BaseModel):
    model: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    file_ids: Optional[list] = Field(default=None, sa_column=Column(JSON))
    instructions: Optional[str] = Field(default=None, max_length=32768, sa_column=Column(TEXT))
    metadata_: Optional[dict] = Field(default=None, sa_column=Column("metadata", JSON))
    name: Optional[str] = Field(default=None)
    tools: Optional[list] = Field(default=None, sa_column=Column(JSON))
    extra_body: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    response_format: Optional[str] = Field(default=None)  # 响应格式
    tool_resources: Optional[dict] = Field(default=None, sa_column=Column(JSON))  # 工具资源
    temperature: Optional[float] = Field(default=None)  # 温度
    top_p: Optional[float] = Field(default=None)  # top_p
