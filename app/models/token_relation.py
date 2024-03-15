from enum import Enum
from sqlmodel import Field

from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin


class RelationType(str, Enum):
    Assistant = "assistant"
    File = "file"
    Thread = "thread"
    Action = "action"


class TokenRelationBase(BaseModel):
    token_id: str = Field(nullable=False)
    relation_type: RelationType = Field(nullable=False)
    relation_id: str = Field(nullable=False)


class TokenRelation(TokenRelationBase, TimeStampMixin, PrimaryKeyMixin, table=True):
    pass


class TokenRelationQuery(TokenRelationBase):
    pass


class TokenRelationDelete(BaseModel):
    relation_type: RelationType = Field(nullable=False)
    relation_id: str = Field(nullable=False)
