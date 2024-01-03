from abc import ABC, abstractmethod
from typing import List, Union, Generator, Tuple, Optional

from fastapi import UploadFile
from sqlmodel import Session

from app.models import File
from app.schemas.common import DeleteResponse


class BaseFileService(ABC):
    @staticmethod
    @abstractmethod
    def get_file_list_by_ids(*, session: Session, file_ids: List[str]) -> List[File]:
        pass

    @staticmethod
    @abstractmethod
    def get_file_list(*, session: Session, purpose: str, file_ids: Optional[List[str]]) -> List[File]:
        pass

    @staticmethod
    @abstractmethod
    def create_file(*, session: Session, purpose: str, file: UploadFile) -> File:
        pass

    @staticmethod
    @abstractmethod
    def get_file(*, session: Session, file_id: str) -> File:
        pass

    @staticmethod
    @abstractmethod
    def get_file_content(*, session: Session, file_id: str) -> Tuple[Union[bytes, Generator], str]:
        pass

    @staticmethod
    @abstractmethod
    def delete_file(*, session: Session, file_id: str) -> DeleteResponse:
        pass
