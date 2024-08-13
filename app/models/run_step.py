from datetime import datetime
from typing import Optional

from pydantic import Field as PDField

from sqlalchemy import Index, Column, Enum
from sqlmodel import Field, JSON

from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin


class RunStepBase(BaseModel):
    status: str = Field(
        sa_column=Column(Enum("cancelled", "completed", "expired", "failed", "in_progress"), nullable=False)
    )
    type: str = Field(sa_column=Column(Enum("message_creation", "tool_calls"), nullable=False))
    assistant_id: str = Field(nullable=False)
    thread_id: str = Field(nullable=False)
    run_id: str = Field(nullable=False)
    object: str = Field(nullable=False, default="thread.run.step")
    metadata_: Optional[dict] = Field(default=None, sa_column=Column("metadata", JSON), schema_extra={"validation_alias": "metadata"})
    last_error: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    step_details: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    completed_at: Optional[datetime] = Field(default=None)
    cancelled_at: Optional[datetime] = Field(default=None)
    expires_at: Optional[datetime] = Field(default=None)
    failed_at: Optional[datetime] = Field(default=None)
    message_id: Optional[str] = Field(default=None)


class RunStep(RunStepBase, PrimaryKeyMixin, TimeStampMixin, table=True):
    __table_args__ = (
        Index("run_step_run_id_idx", "run_id"),
        Index("run_step_run_id_type_idx", "run_id", "type"),
    )


class RunStepRead(RunStepBase, PrimaryKeyMixin, TimeStampMixin):
    metadata_: Optional[dict] = PDField(default=None, alias="metadata")
