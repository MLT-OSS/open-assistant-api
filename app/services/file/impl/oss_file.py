import uuid
from typing import List, Union, Generator, Tuple

from fastapi import UploadFile
from sqlmodel import Session, select, col, desc

from app.exceptions.exception import ResourceNotFoundError
from app.models import File
from app.providers.storage import storage
from app.schemas.common import DeleteResponse
from app.services.file.file import BaseFileService


class OSSFileService(BaseFileService):
    @staticmethod
    def get_file_list_by_ids(*, session: Session, file_ids: List[str]) -> List[File]:
        if not file_ids:
            return []
        statement = select(File).where(col(File.id).in_(file_ids))
        return session.exec(statement).all()

    @staticmethod
    def get_file_list(*, session: Session, purpose: str, file_ids: List[str]) -> List[File]:
        statement = select(File)
        if purpose is not None and len(purpose) > 0:
            statement = statement.where(File.purpose == purpose)
        if file_ids is not None:
            statement = statement.where(File.id.in_(file_ids))
        statement = statement.order_by(desc(File.created_at))
        return session.exec(statement).all()

    @staticmethod
    def create_file(*, session: Session, purpose: str, file: UploadFile) -> File:
        # 文件是否存在
        statement = (
            select(File)
            .where(File.purpose == purpose)
            .where(File.filename == file.filename)
            .where(File.bytes == file.size)
        )
        ext_file = session.exec(statement).first()
        if ext_file is not None:
            # TODO: 文件去重策略
            return ext_file

        key = f"{uuid.uuid4()}-{file.filename}"
        storage.save(filename=key, data=file.file.read())

        # 存储
        db_file = File(purpose=purpose, filename=file.filename, bytes=file.size, key=key)
        session.add(db_file)
        session.commit()
        session.refresh(db_file)
        return db_file

    @staticmethod
    def get_file(*, session: Session, file_id: str) -> File:
        statement = select(File).where(File.id == file_id)
        ext_file = session.exec(statement).one_or_none()
        if ext_file is None:
            raise ResourceNotFoundError(message="File not found")
        return ext_file

    @staticmethod
    def get_file_content(*, session: Session, file_id: str) -> Tuple[Union[bytes, Generator], str]:
        ext_file = OSSFileService.get_file(session=session, file_id=file_id)
        if not ext_file:
            raise ResourceNotFoundError(message="File not found")
        file_data = storage.load(ext_file.key)
        return file_data, ext_file.filename

    @staticmethod
    def delete_file(*, session: Session, file_id: str) -> DeleteResponse:
        ext_file = OSSFileService.get_file(session=session, file_id=file_id)
        # TODO 删除s3文件

        # 删除记录
        session.delete(ext_file)
        session.commit()
        return DeleteResponse(id=file_id, deleted=True)
