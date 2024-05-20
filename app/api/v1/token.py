from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.deps import verify_admin_token, get_async_session
from app.libs.paginate import CommonPage, cursor_page
from app.models.token import Token, TokenCreate, TokenUpdate
from app.services.token.token import TokenService

router = APIRouter()


@router.get("", response_model=CommonPage[Token], dependencies=[Depends(verify_admin_token)])
async def list_tokens(*, session: AsyncSession = Depends(get_async_session)):
    """
    Returns a list of tokens.
    """
    statement = select(Token)
    return await cursor_page(statement, session)


@router.post("", response_model=Token, dependencies=[Depends(verify_admin_token)])
async def create_token(*, session: AsyncSession = Depends(get_async_session), body: TokenCreate) -> Token:
    """
    Create a token with a llm url & token.
    """
    return await TokenService.create_token(session=session, body=body)


@router.get("/{token}", response_model=Token, dependencies=[Depends(verify_admin_token)])
async def get_token(*, session: AsyncSession = Depends(get_async_session), token: str) -> Token:
    """
    Retrieves a token.
    """
    return await TokenService.get_token(session=session, token=token)


@router.get("/refresh_token/{token}", response_model=Token, dependencies=[Depends(verify_admin_token)])
async def refresh_token(*, session: AsyncSession = Depends(get_async_session), token: str) -> Token:
    return await TokenService.refresh_token(session=session, token=token)


@router.post("/modify_token/{token}", response_model=Token, dependencies=[Depends(verify_admin_token)])
async def modify_token(*, session: AsyncSession = Depends(get_async_session), body: TokenUpdate, token: str) -> Token:
    return await TokenService.modify_token(session=session, body=body, token=token)
