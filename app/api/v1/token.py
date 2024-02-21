from sqlmodel import Session, select
from fastapi import APIRouter, Depends

from app.api.deps import get_session, verify_admin_token
from app.libs.paginate import CommonPage, cursor_page
from app.models.token import Token, TokenCreate, TokenUpdate
from app.services.token.token import TokenService

router = APIRouter()


@router.get("/list", response_model=CommonPage[Token], dependencies=[Depends(verify_admin_token)])
def list_tokens(*, session: Session = Depends(get_session)):
    """
    Returns a list of tokens.
    """
    statement = select(Token)
    return cursor_page(statement, session)


@router.post("", response_model=Token, dependencies=[Depends(verify_admin_token)])
def create_token(*, session: Session = Depends(get_session), body: TokenCreate) -> Token:
    """
    Create a token with a llm url & token.
    """
    return TokenService.create_token(session=session, body=body)


@router.get("", response_model=Token, dependencies=[Depends(verify_admin_token)])
def get_token(*, session: Session = Depends(get_session), token: str) -> Token:
    """
    Retrieves a token.
    """
    return TokenService.get_token(session=session, token=token)


@router.get("/refresh_token", response_model=Token, dependencies=[Depends(verify_admin_token)])
def refresh_token(*, session: Session = Depends(get_session), token: str) -> Token:
    return TokenService.refresh_token(session=session, token=token)


@router.post("/modify_token", response_model=Token, dependencies=[Depends(verify_admin_token)])
def modify_token(*, session: Session = Depends(get_session), update: TokenUpdate) -> Token:
    return TokenService.modify_token(session=session, update=update)
