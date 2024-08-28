from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exception import ResourceNotFoundError
from app.models.assistant import Assistant, AssistantUpdate, AssistantCreate
from app.models.token_relation import RelationType
from app.providers.auth_provider import auth_policy
from app.schemas.common import DeleteResponse
from app.utils import revise_tool_names


class AssistantService:
    @staticmethod
    async def create_assistant(*, session: AsyncSession, body: AssistantCreate, token_id: str = None) -> Assistant:
        revise_tool_names(body.tools)
        db_assistant = Assistant.model_validate(body.model_dump(by_alias=True))
        session.add(db_assistant)
        auth_policy.insert_token_rel(
            session=session, token_id=token_id, relation_type=RelationType.Assistant, relation_id=db_assistant.id
        )
        await session.commit()
        await session.refresh(db_assistant)
        return db_assistant

    @staticmethod
    async def modify_assistant(*, session: AsyncSession, assistant_id: str, body: AssistantUpdate) -> Assistant:
        revise_tool_names(body.tools)
        db_assistant = await AssistantService.get_assistant(session=session, assistant_id=assistant_id)
        update_data = body.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_assistant, key, value)
        session.add(db_assistant)
        await session.commit()
        await session.refresh(db_assistant)
        return db_assistant

    @staticmethod
    async def delete_assistant(
        *,
        session: AsyncSession,
        assistant_id: str,
    ) -> DeleteResponse:
        db_ass = await AssistantService.get_assistant(session=session, assistant_id=assistant_id)
        await session.delete(db_ass)
        await auth_policy.delete_token_rel(
            session=session, relation_type=RelationType.Assistant, relation_id=assistant_id
        )
        await session.commit()
        return DeleteResponse(id=assistant_id, object="assistant.deleted", deleted=True)

    @staticmethod
    async def get_assistant(*, session: AsyncSession, assistant_id: str) -> Assistant:
        statement = select(Assistant).where(Assistant.id == assistant_id)
        result = await session.execute(statement)
        assistant = result.scalars().one_or_none()
        if assistant is None:
            raise ResourceNotFoundError(message="Assistant not found")
        return assistant

    @staticmethod
    def get_assistant_sync(*, session: AsyncSession, assistant_id: str) -> Assistant:
        statement = select(Assistant).where(Assistant.id == assistant_id)
        result = session.execute(statement)
        assistant = result.scalars().one_or_none()
        if assistant is None:
            raise ResourceNotFoundError(message="Assistant not found")
        return assistant
