import tempfile
import uuid
from typing import List

import aiofiles
import aiofiles.os
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import File
from app.providers.r2r import r2r
from app.providers.storage import storage
from app.services.file.impl.oss_file import OSSFileService


class R2RFileService(OSSFileService):
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

        file_key = f"{uuid.uuid4()}-{file.filename}"
        with tempfile.NamedTemporaryFile(suffix='_' + file.filename, delete=True) as temp_file:
            tmp_file_path = temp_file.name

            async with aiofiles.open(tmp_file_path, 'wb') as f:
                while content := await file.read(1024):
                    await f.write(content)

            storage.save_from_path(filename=file_key, local_file_path=tmp_file_path)

            r2r.ingest_file(file_path=tmp_file_path, metadata={"file_key": file_key})

        # 存储
        db_file = File(purpose=purpose, filename=file.filename, bytes=file.size, key=file_key)
        session.add(db_file)
        await session.commit()
        await session.refresh(db_file)
        return db_file

    @staticmethod
    def search_in_files(query: str, file_keys: List[str]) -> dict:
        files = {}
        search_results = r2r.search(query, filters={"file_key": {"$in": file_keys}})
        if not search_results:
            return files

        for doc in search_results:
            file_key = doc.get("metadata").get("file_key")
            text = doc.get("text")
            if file_key in files and files[file_key]:
                files[file_key] += f"\n\n{text}"
            else:
                files[file_key] = doc.get("text")

        return files

    # TODO 删除s3&r2r文件
