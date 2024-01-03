from typing import List
from pydantic import BaseModel

from app.models import File


class ListFilesResponse(BaseModel):
    data: List[File]
    object: str = "file"
