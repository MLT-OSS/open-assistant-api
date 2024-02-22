from typing import Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field

from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin


class ActionBase(BaseModel):
    name: str = Field(nullable=False)
    description: Optional[str] = Field(nullable=False)
    openapi_schema: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    authentication: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    extra: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    metadata_: Optional[dict] = Field(default=None, sa_column=Column("metadata", JSON))
    operation_id: str = Field(nullable=False)
    url: str = Field(nullable=False)
    method: str = Field(nullable=False)
    path_param_schema: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    query_param_schema: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    body_param_schema: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    body_type: str = Field(nullable=False)
    function_def: Optional[dict] = Field(default=None, sa_column=Column(JSON))


class Action(ActionBase, PrimaryKeyMixin, TimeStampMixin, table=True):

    object: str = Field(nullable=False, default="action")
