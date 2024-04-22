from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exception import ResourceNotFoundError
from app.models.assistant_file import (
    AssistantFile,
    AssistantFileCreate,
    AssistantFileUpdate,
)
from app.schemas.common import DeleteResponse


class AssistantFileService:
    @staticmethod
    async def create_assistant_file(
        *, session: AsyncSession, assistant_id: str, body: AssistantFileCreate
    ) -> AssistantFile:
        # TODO 关系表暂时不实现
        return AssistantFile(id="", assistant_id=assistant_id)

    @staticmethod
    async def modify_assistant_file(
        *, session: AsyncSession, assistant_id: str, body: AssistantFileUpdate
    ) -> AssistantFile:
        db_assistant = await AssistantFileService.get_assistant_file(
            session=session, assistant_id=assistant_id, file_id=body.id
        )
        update_data = body.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_assistant, key, value)
        session.add(db_assistant)
        await session.commit()
        await session.refresh(db_assistant)
        return db_assistant

    @staticmethod
    async def delete_assistant_file(*, session: AsyncSession, assistant_id: str, file_id: str) -> DeleteResponse:
        assistant_file = await AssistantFileService.get_assistant_file(
            session=session, assistant_id=assistant_id, file_id=file_id
        )
        id = assistant_file.id
        await session.delete(assistant_file)
        await session.commit()
        return DeleteResponse(id=id, object="assistant_file.deleted", deleted=True)

    @staticmethod
    async def get_assistant_file(*, session: AsyncSession, assistant_id: str, file_id: str) -> AssistantFile:
        statement = select(AssistantFile).where(AssistantFile.id == assistant_id).where(AssistantFile.id == file_id)
        result = await session.execute(statement)
        assistant_file = result.scalars().one_or_none()
        if assistant_file is None:
            raise ResourceNotFoundError(message=f"Assistant file-{file_id} not found")
        return session.exec(statement).one_or_none()
