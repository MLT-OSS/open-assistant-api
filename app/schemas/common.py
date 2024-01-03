from pydantic import BaseModel


class DeleteResponse(BaseModel):
    id: str
    object: str = "file"
    deleted: bool
