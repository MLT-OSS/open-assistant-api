from abc import ABC, abstractmethod
from typing import List, Union, Generator, Tuple, Optional

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import UploadFile

from app.models import File
from app.schemas.common import DeleteResponse


class BaseFileService(ABC):
    @staticmethod
    @abstractmethod
    def get_file_list_by_ids(*, session: Session, file_ids: List[str]) -> List[File]:
        pass

    @staticmethod
    @abstractmethod
    async def get_file_list(*, session: AsyncSession, purpose: str, file_ids: Optional[List[str]]) -> List[File]:
        pass

    @staticmethod
    @abstractmethod
    async def create_file(*, session: AsyncSession, purpose: str, file: UploadFile) -> File:
        pass

    @staticmethod
    @abstractmethod
    async def get_file(*, session: AsyncSession, file_id: str) -> File:
        pass

    @staticmethod
    @abstractmethod
    async def get_file_content(*, session: AsyncSession, file_id: str) -> Tuple[Union[bytes, Generator], str]:
        pass

    @staticmethod
    @abstractmethod
    async def delete_file(*, session: AsyncSession, file_id: str) -> DeleteResponse:
        pass

    @staticmethod
    @abstractmethod
    def search_in_files(*, query: str, file_keys: List[str]) -> dict:
        pass
