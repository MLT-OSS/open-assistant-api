from datetime import datetime
from typing import Optional, Any, Union

from pydantic import Field as PDField

from sqlalchemy import Column, Enum
from sqlalchemy.sql.sqltypes import JSON, TEXT
from sqlmodel import Field

from pydantic import model_validator

from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin
from app.models.message import MessageCreate
from app.schemas.tool.authentication import Authentication


class RunBase(BaseModel):
    instructions: Optional[str] = Field(default=None, max_length=32768, sa_column=Column(TEXT))
    model: Optional[str] = Field(default=None)
    status: str = Field(
        default="queued",
        sa_column=Column(
            Enum(
                "cancelled",
                "cancelling",
                "completed",
                "expired",
                "failed",
                "in_progress",
                "queued",
                "requires_action",
            ),
            default="queued",
            nullable=True,
        ),
    )
    assistant_id: str = Field(nullable=False)
    thread_id: str = Field(default=None, nullable=False)
    object: str = Field(nullable=False, default="thread.run")
    file_ids: Optional[list] = Field(default=[], sa_column=Column(JSON))
    metadata_: Optional[dict] = Field(default=None, sa_column=Column("metadata", JSON), schema_extra={"validation_alias": "metadata"})
    last_error: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    required_action: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    tools: Optional[list] = Field(default=[], sa_column=Column(JSON))
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    cancelled_at: Optional[datetime] = Field(default=None)
    expires_at: Optional[datetime] = Field(default=None)
    failed_at: Optional[datetime] = Field(default=None)
    additional_instructions: Optional[str] = Field(default=None, max_length=32768, sa_column=Column(TEXT))
    extra_body: Optional[dict] = Field(default={}, sa_column=Column(JSON))
    stream_options: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    incomplete_details: Optional[str] = Field(default=None)  # 未完成详情
    max_completion_tokens: Optional[int] = Field(default=None)  # 最大完成长度
    max_prompt_tokens: Optional[int] = Field(default=None)  # 最大提示长度
    response_format: Optional[Union[str, dict]] = Field(default="auto", sa_column=Column(JSON))  # 响应格式
    tool_choice: Optional[str] = Field(default=None)  # 工具选择
    truncation_strategy: Optional[dict] = Field(default=None, sa_column=Column(JSON))  # 截断策略
    usage: Optional[dict] = Field(default=None, sa_column=Column(JSON))  # 调用使用情况
    temperature: Optional[float] = Field(default=None)  # 温度
    top_p: Optional[float] = Field(default=None)  # top_p


class Run(RunBase, PrimaryKeyMixin, TimeStampMixin, table=True):
    pass


class RunCreate(BaseModel):
    assistant_id: str
    status: Optional[str] = "queued"
    instructions: Optional[str] = None
    additional_instructions: Optional[str] = None
    model: Optional[str] = None
    metadata_: Optional[dict] = Field(default=None, schema_extra={"validation_alias": "metadata"})
    tools: Optional[list] = []
    extra_body: Optional[dict[str, Union[dict[str, Union[Authentication, Any]], Any]]] = {}
    stream: Optional[bool] = False
    stream_options: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    additional_messages: Optional[list[MessageCreate]] = Field(default=[], sa_column=Column(JSON))  # 消息列表
    max_completion_tokens: Optional[int] = None  # 最大完成长度
    max_prompt_tokens: Optional[int] = Field(default=None)  # 最大提示长度
    truncation_strategy: Optional[dict] = Field(default=None, sa_column=Column(JSON))  # 截断策略
    response_format: Optional[Union[str, dict]] = Field(default="auto", sa_column=Column(JSON))  # 响应格式
    tool_choice: Optional[str] = Field(default=None)  # 工具选择
    temperature: Optional[float] = Field(default=None)  # 温度
    top_p: Optional[float] = Field(default=None)  # top_p

    @model_validator(mode="before")
    def model_validator(cls, data: Any):
        extra_body = data.get("extra_body")
        if extra_body:
            action_authentications = extra_body.get("action_authentications")
            if action_authentications:
                res = action_authentications.values()
                [Authentication.model_validate(i).encrypt() for i in res]
        return data


class RunUpdate(BaseModel):
    tools: Optional[list] = []
    metadata_: Optional[dict] = Field(default=None, schema_extra={"validation_alias": "metadata"})
    extra_body: Optional[dict[str, Authentication]] = {}

    @model_validator(mode="before")
    def model_validator(cls, data: Any):
        extra_body = data.get("extra_body")
        if extra_body:
            action_authentications = extra_body.get("action_authentications")
            if action_authentications:
                res = action_authentications.values()
                [Authentication.model_validate(i).encrypt() for i in res]
        return data


class RunRead(RunBase, TimeStampMixin, PrimaryKeyMixin):
    metadata_: Optional[dict] = PDField(default=None, alias="metadata")
