from datetime import datetime
from typing import Optional

import orjson
from sqlalchemy import DateTime, text
from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel, Field

from app.libs.types import ObjectId
from app.libs.util import datetime2timestamp


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


def to_snake_case(string: str) -> str:
    return "".join(["_" + i.lower() if i.isupper() else i for i in string]).lstrip("_")


class BaseModel(SQLModel):
    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: datetime2timestamp(v),
        }

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return to_snake_case(cls.__name__)


class TimeStampMixin(SQLModel):
    created_at: Optional[datetime] = Field(
        sa_type=DateTime, default=None, nullable=False,  sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
    updated_at: Optional[datetime] = Field(
        sa_type=DateTime, default=None, sa_column_kwargs={"onupdate": text("CURRENT_TIMESTAMP")}
    )


class PrimaryKeyMixin(SQLModel):
    id: str = Field(primary_key=True, default_factory=ObjectId)
