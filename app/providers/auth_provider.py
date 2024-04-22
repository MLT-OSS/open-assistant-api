import logging
from fastapi import Depends

from sqlmodel import select

from app.api.deps import verfiy_token, verify_token_relation
from app.models.token_relation import RelationType, TokenRelation, TokenRelationDelete
from app.services.token.token_relation import TokenRelationService
from config.config import settings


class AuthPolicy(object):
    """
    default auth policy with nothing to do
    """

    def enable(self):
        """
        enable auth policy
        """

    def insert_token_rel(self, session, token_id: str, relation_type: RelationType, relation_id: str):
        """
        insert a token relation to database when enable token auth policy
        """

    async def delete_token_rel(self, session, relation_type: RelationType, relation_id: str):
        """
        delete token relation when enable token auth policy
        """

    def token_filter(self, statement, field, relation_type: RelationType, token_id: str):
        """
        add token filter clause when enable token auth policy
        """
        return statement


class SimpleTokenAuthPolicy(AuthPolicy):
    """
    simple token auth policy
    """

    def enable(self):
        """
        add auth verify dependents to path router
        """
        from app.api.v1 import assistant, assistant_file, thread, message, runs, action

        verify_assistant_depends = Depends(
            verify_token_relation(relation_type=RelationType.Assistant, name="assistant_id")
        )
        # assistant router
        for route in assistant.router.routes:
            if route.name == assistant.create_assistant.__name__ or route.name == assistant.list_assistants.__name__:
                route.dependencies.append(Depends(verfiy_token))
            else:
                route.dependencies.append(verify_assistant_depends)

        # thread router
        verify_thread_depends = Depends(verify_token_relation(relation_type=RelationType.Thread, name="thread_id"))
        for route in thread.router.routes:
            if route.name == thread.create_thread.__name__:
                route.dependencies.append(
                    Depends(
                        verify_token_relation(
                            relation_type=RelationType.Thread, name="thread_id", ignore_none_relation_id=True
                        )
                    )
                )
            else:
                route.dependencies.append(verify_thread_depends)

        # action router
        verify_action_depends = Depends(verify_token_relation(relation_type=RelationType.Action, name="action_id"))
        for route in action.router.routes:
            if route.name == action.create_actions.__name__ or route.name == action.list_actions.__name__:
                route.dependencies.append(Depends(verfiy_token))
            else:
                route.dependencies.append(verify_action_depends)

        self.__append_deps_for_all_routes(assistant_file.router, verify_assistant_depends)
        self.__append_deps_for_all_routes(message.router, verify_thread_depends)
        self.__append_deps_for_all_routes(runs.router, verify_thread_depends)

    def insert_token_rel(self, session, token_id: str, relation_type: RelationType, relation_id: str):
        if token_id:
            relation = TokenRelation(token_id=token_id, relation_type=relation_type, relation_id=str(relation_id))
            session.add(relation)

    async def delete_token_rel(self, session, relation_type: RelationType, relation_id: str):
        to_delete = TokenRelationDelete(relation_type=relation_type, relation_id=relation_id)
        relation = await TokenRelationService.get_relation_to_delete(session=session, delete=to_delete)
        await session.delete(relation)

    def token_filter(self, statement, field, relation_type: RelationType, token_id: str):
        id_subquery = select(TokenRelation.relation_id).where(
            TokenRelation.relation_type == relation_type, TokenRelation.token_id == token_id
        )
        return statement.where(field.in_(id_subquery))

    def __append_deps_for_all_routes(self, router, depends):
        for route in router.routes:
            route.dependencies.append(depends)


auth_policy: AuthPolicy = SimpleTokenAuthPolicy() if settings.AUTH_ENABLE else AuthPolicy()


def register(app):
    logging.info("use auth polily: %s", auth_policy.__class__.__name__)
    auth_policy.enable()
