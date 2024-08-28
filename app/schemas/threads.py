from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field

from app.models.thread import ThreadCreate


class CreateThreadAndRun(BaseModel):
    assistant_id: str
    thread: Optional[ThreadCreate] = None
    instructions: Optional[str] = None
    model: Optional[str] = None
    metadata_: Optional[dict] = Field(default=None, schema_extra={"validation_alias": "metadata"})
    tools: Optional[list] = Field(default=[])
    stream: Optional[bool] = False
