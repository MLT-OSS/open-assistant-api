from typing import Optional

import orjson
from sqlalchemy import Column, DateTime, text
from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel, Field

from app.libs.types import ObjectId
from app.libs.types import Timestamp


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


def to_snake_case(string: str) -> str:
    return "".join(["_" + i.lower() if i.isupper() else i for i in string]).lstrip("_")


class BaseModel(SQLModel):
    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return to_snake_case(cls.__name__)


class TimeStampMixin(SQLModel):
    created_at: Optional[Timestamp] = Field(
        sa_column=Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    )
    updated_at: Optional[Timestamp] = Field(
        sa_column=Column(DateTime, server_default=text("null"), onupdate=text("CURRENT_TIMESTAMP"))
    )


class PrimaryKeyMixin(SQLModel):
    id: str = Field(primary_key=True, default_factory=ObjectId)
