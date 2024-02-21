from sqlmodel import Session, select

from app.models.token_relation import RelationType, TokenRelation, TokenRelationDelete, TokenRelationQuery


class TokenRelationService:
    @staticmethod
    def get_relation(session: Session, query: TokenRelationQuery) -> bool:
        statement = select(TokenRelation).where(
            TokenRelation.token_id == query.token_id,
            TokenRelation.relation_id == query.relation_id,
            TokenRelation.relation_type == query.relation_type,
        )
        record = session.exec(statement).one_or_none()
        return record

    @staticmethod
    def get_relation_to_delete(session: Session, delete: TokenRelationDelete) -> bool:
        statement = select(TokenRelation).where(
            TokenRelation.relation_id == delete.relation_id, TokenRelation.relation_type == delete.relation_type
        )
        record = session.exec(statement).one_or_none()
        return record

    @staticmethod
    def get_token_id_by_relation(session: Session, relation_type: RelationType, relation_id: str) -> bool:
        statement = select(TokenRelation.token_id).where(
            TokenRelation.relation_id == relation_id, TokenRelation.relation_type == relation_type
        )
        return session.exec(statement).one_or_none()

    @staticmethod
    def verify_relation(session: Session, verify: TokenRelationQuery) -> bool:
        record = TokenRelationService.get_relation(session, verify)
        return record is not None
