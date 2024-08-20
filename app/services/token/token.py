from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.exceptions.exception import ResourceNotFoundError
from app.libs import util

from app.models.token import Token, TokenCreate, TokenUpdate


class TokenService:
    @staticmethod
    async def create_token(session: AsyncSession, body: TokenCreate) -> Token:
        db_token = Token.model_validate(body.model_dump(by_alias=True))
        session.add(db_token)
        await session.commit()
        await session.refresh(db_token)
        return db_token

    @staticmethod
    async def get_token(session: AsyncSession, token: str) -> Token:
        statement = select(Token).where(Token.assistant_token == token)
        result = await session.execute(statement)
        token = result.scalars().one_or_none()
        if token is None:
            raise ResourceNotFoundError(message="Token not found")
        return token

    @staticmethod
    def get_token_by_id(session: Session, token_id: str) -> Token:
        statement = select(Token).where(Token.id == token_id)
        result = session.execute(statement)
        token = result.scalars().one_or_none()
        if token is None:
            raise ResourceNotFoundError(message="Token not found")
        return token

    @staticmethod
    async def refresh_token(session: AsyncSession, token) -> Token:
        db_token = await TokenService.get_token(session=session, token=token)
        db_token.assistant_token = util.random_uuid()
        session.add(db_token)
        await session.commit()
        await session.refresh(db_token)
        return db_token

    @staticmethod
    async def modify_token(session: AsyncSession, body: TokenUpdate, token: str) -> Token:
        db_token = await TokenService.get_token(session=session, token=token)
        for key, value in body.model_dump(exclude_unset=True).items():
            setattr(db_token, key, value)
        session.add(db_token)
        await session.commit()
        await session.refresh(db_token)
        return db_token
