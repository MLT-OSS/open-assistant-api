from typing import AsyncGenerator

from fastapi import Depends, Request
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exception import AuthenticationError, AuthorizationError, ResourceNotFoundError
from app.models.token import Token
from app.models.token_relation import RelationType, TokenRelationQuery
from app.providers import database
from app.services.token.token import TokenService
from app.services.token.token_relation import TokenRelationService
from config.config import settings


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """session生成器 作为fast api的Depends选项"""
    async with database.async_session_local() as session:
        yield session


class OAuth2Bearer(APIKeyHeader):
    """
    it use to fetch token from header
    """

    def __init__(
        self, *, name: str, scheme_name: str | None = None, description: str | None = None, auto_error: bool = True
    ):
        super().__init__(name=name, scheme_name=scheme_name, description=description, auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        authorization_header_value = request.headers.get(self.model.name)
        if authorization_header_value:
            scheme, _, param = authorization_header_value.partition(" ")
            if scheme.lower() == "bearer" and param.strip() != "":
                return param.strip()
        return None


oauth_token = OAuth2Bearer(name="Authorization")


async def verify_admin_token(token=Depends(oauth_token)) -> Token:
    """
    admin token authentication
    """
    if token is None:
        raise AuthenticationError()
    if settings.AUTH_ADMIN_TOKEN != token:
        raise AuthorizationError()


async def get_token(session=Depends(get_async_session), token=Depends(oauth_token)) -> Token:
    """
    get token info
    """
    if token and token != "":
        try:
            return await TokenService.get_token(session=session, token=token)
        except ResourceNotFoundError:
            pass
    return None


async def verfiy_token(token: Token = Depends(get_token)):
    if token is None:
        raise AuthenticationError()


async def get_token_id(token: Token = Depends(get_token)):
    """
    Return token_id, which can be considered as user information.
    """
    return token.id if token is not None else None


def get_param(name: str):
    """
    extract param from Request
    """

    async def get_param_from_request(request: Request):
        if name in request.path_params:
            return request.path_params[name]
        if name in request.query_params:
            return request.query_params[name]
        body = await request.json()
        if name in body:
            return body[name]

    return get_param_from_request


def verify_token_relation(relation_type: RelationType, name: str, ignore_none_relation_id: bool = False):
    """
    param relation_type: relation type
    param name: param name
    param ignore_none_relation_id: if ignore_none_relation_id is set, return where relation_id is None, use for copy thread api
    """

    async def verify_authorization(
        session=Depends(get_async_session), token_id=Depends(get_token_id), relation_id=Depends(get_param(name))
    ):
        if token_id and ignore_none_relation_id:
            return
        if token_id and relation_id:
            verify = TokenRelationQuery(token_id=token_id, relation_type=relation_type, relation_id=relation_id)
            if await TokenRelationService.verify_relation(session=session, verify=verify):
                return
        raise AuthorizationError()

    return verify_authorization
