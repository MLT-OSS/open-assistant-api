from pydantic import BaseModel, Field
from typing import Optional, Any


class DeleteResponse(BaseModel):
    id: str
    object: str = "file"
    deleted: bool


class BaseSuccessDataResponse(BaseModel):
    status: str = Field("success")
    data: Optional[Any] = None
