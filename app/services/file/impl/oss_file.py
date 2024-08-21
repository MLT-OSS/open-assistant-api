import tempfile
import uuid
from typing import List, Union, Generator, Tuple

import aiofiles
import aiofiles.os
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlmodel import select, col, desc

from app.exceptions.exception import ResourceNotFoundError
from app.models import File
from app.providers.r2r import r2r
from app.providers.storage import storage
from app.schemas.common import DeleteResponse
from app.services.file.file import BaseFileService


class OSSFileService(BaseFileService):
    @staticmethod
    def get_file_list_by_ids(*, session: Session, file_ids: List[str]) -> List[File]:
        if not file_ids:
            return []
        statement = select(File).where(col(File.id).in_(file_ids))
        return session.execute(statement).scalars().all()

    @staticmethod
    async def get_file_list(*, session: AsyncSession, purpose: str, file_ids: List[str]) -> List[File]:
        statement = select(File)
        if purpose is not None and len(purpose) > 0:
            statement = statement.where(File.purpose == purpose)
        if file_ids is not None:
            statement = statement.where(File.id.in_(file_ids))
        statement = statement.order_by(desc(File.created_at))
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def create_file(*, session: AsyncSession, purpose: str, file: UploadFile) -> File:
        # 文件是否存在
        # statement = (
        #     select(File)
        #     .where(File.purpose == purpose)
        #     .where(File.filename == file.filename)
        #     .where(File.bytes == file.size)
        # )
        # result = await session.execute(statement)
        # ext_file = result.scalars().first()
        # if ext_file is not None:
        #     # TODO: 文件去重策略
        #     return ext_file

        file_suffix = '_' + file.filename
        with tempfile.NamedTemporaryFile(suffix=file_suffix, delete=True) as temp_file:
            tmp_file_path = temp_file.name
            key = f"{uuid.uuid4()}-{file.filename}"

            async with aiofiles.open(tmp_file_path, 'wb') as f:
                while content := await file.read(1024):
                    await f.write(content)

            storage.save_from_path(filename=key, local_file_path=tmp_file_path)

            r2r.ingest_file(file_path=tmp_file_path, metadata={"oai_file_key": key})

        # 存储
        db_file = File(purpose=purpose, filename=file.filename, bytes=file.size, key=key)
        session.add(db_file)
        await session.commit()
        await session.refresh(db_file)
        return db_file

    @staticmethod
    async def get_file(*, session: AsyncSession, file_id: str) -> File:
        statement = select(File).where(File.id == file_id)
        result = await session.execute(statement)
        ext_file = result.scalars().one_or_none()
        if ext_file is None:
            raise ResourceNotFoundError(message="File not found")
        return ext_file

    @staticmethod
    async def get_file_content(*, session: AsyncSession, file_id: str) -> Tuple[Union[bytes, Generator], str]:
        ext_file = await OSSFileService.get_file(session=session, file_id=file_id)
        file_data = storage.load(ext_file.key)
        return file_data, ext_file.filename

    @staticmethod
    async def delete_file(*, session: AsyncSession, file_id: str) -> DeleteResponse:
        ext_file = await OSSFileService.get_file(session=session, file_id=file_id)
        # TODO 删除s3&r2r文件

        # 删除记录
        await session.delete(ext_file)
        await session.commit()
        return DeleteResponse(id=file_id, deleted=True)
