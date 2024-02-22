from sqlmodel import Session, select
from app.exceptions.exception import ResourceNotFoundError
from app.libs import util

from app.models.token import Token, TokenCreate, TokenUpdate


class TokenService:
    @staticmethod
    def create_token(session: Session, body: TokenCreate) -> Token:
        db_token = Token.model_validate(body)
        session.add(db_token)
        session.commit()
        session.refresh(db_token)
        return db_token

    @staticmethod
    def get_token(session: Session, token: str) -> Token:
        statement = select(Token).where(Token.assistant_token == token)
        token = session.exec(statement).one_or_none()
        if token is None:
            raise ResourceNotFoundError(message="Token not found")
        return token

    @staticmethod
    def get_token_by_id(session: Session, token_id: str) -> Token:
        statement = select(Token).where(Token.id == token_id)
        token = session.exec(statement).one_or_none()
        if token is None:
            raise ResourceNotFoundError(message="Token not found")
        return token

    @staticmethod
    def refresh_token(session: Session, token) -> Token:
        db_token = TokenService.get_token(session=session, token=token)
        db_token.assistant_token = util.random_uuid()
        session.add(db_token)
        session.commit()
        session.refresh(db_token)
        return db_token

    @staticmethod
    def modify_token(session: Session, update: TokenUpdate) -> Token:
        db_token = TokenService.get_token(session=session, token=update.assistant_token)
        for key, value in update.model_dump(exclude_unset=True).items():
            setattr(db_token, key, value)
        session.add(db_token)
        session.commit()
        session.refresh(db_token)
        return db_token
