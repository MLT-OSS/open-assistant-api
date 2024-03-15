from typing import Optional, Any

from pydantic import BaseModel, Field


class DeleteResponse(BaseModel):
    id: str
    object: str = "file"
    deleted: bool


class BaseSuccessDataResponse(BaseModel):
    status: str = Field("success")
    data: Optional[Any] = None
