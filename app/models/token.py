from typing import Optional

from sqlalchemy import Index
from sqlmodel import Field
from app.libs import util

from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin


class TokenBase(BaseModel):
    llm_base_url: str = Field(nullable=False)
    llm_api_key: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)


class Token(TokenBase, TimeStampMixin, PrimaryKeyMixin, table=True):
    __table_args__ = (Index("token_assistant_token_idx", "assistant_token", unique=True),)

    assistant_token: str = Field(default_factory=util.random_uuid)


class TokenCreate(TokenBase):
    pass


class TokenUpdate(TokenBase):
    pass
