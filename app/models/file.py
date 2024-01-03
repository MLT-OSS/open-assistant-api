from typing import Optional

from sqlalchemy import Index, Column, Enum
from sqlmodel import Field

from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin


class File(BaseModel, PrimaryKeyMixin, TimeStampMixin, table=True):
    __table_args__ = (Index("file_purpose_idx", "purpose"),)

    bytes: int = Field(nullable=False)
    filename: str = Field(nullable=False)
    purpose: str = Field(nullable=False)
    object: str = Field(nullable=False, default="file")
    key: str = Field(nullable=False)
    status: Optional[str] = Field(default=None, sa_column=Column("status", Enum("error", "processed", "uploaded")))
    status_details: Optional[str] = Field(default=None)
