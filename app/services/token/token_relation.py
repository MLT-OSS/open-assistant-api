from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.models.token_relation import RelationType, TokenRelation, TokenRelationDelete, TokenRelationQuery


class TokenRelationService:
    @staticmethod
    async def get_relation(session: AsyncSession, query: TokenRelationQuery) -> bool:
        statement = select(TokenRelation).where(
            TokenRelation.token_id == query.token_id,
            TokenRelation.relation_id == query.relation_id,
            TokenRelation.relation_type == query.relation_type,
        )
        result = await session.execute(statement)
        record = result.scalars().one_or_none()
        return record

    @staticmethod
    async def get_relation_to_delete(session: AsyncSession, delete: TokenRelationDelete) -> bool:
        statement = select(TokenRelation).where(
            TokenRelation.relation_id == delete.relation_id, TokenRelation.relation_type == delete.relation_type
        )
        result = await session.execute(statement)
        record = result.scalars().one_or_none()
        return record

    @staticmethod
    def get_token_id_by_relation(session: Session, relation_type: RelationType, relation_id: str) -> bool:
        statement = select(TokenRelation.token_id).where(
            TokenRelation.relation_id == relation_id, TokenRelation.relation_type == relation_type
        )
        result = session.execute(statement)
        return result.scalars().one_or_none()

    @staticmethod
    async def verify_relation(session: AsyncSession, verify: TokenRelationQuery) -> bool:
        record = await TokenRelationService.get_relation(session, verify)
        return record is not None
