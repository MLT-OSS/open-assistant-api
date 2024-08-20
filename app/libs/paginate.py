import logging
from typing import TypeVar, Any, Optional, Generic, List, Sequence

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams, CursorRawParams
from fastapi_pagination.cursor import encode_cursor
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi_pagination.types import Cursor
from fastapi_pagination.utils import verify_params, create_pydantic_model
from sqlmodel import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class CursorParams(BaseModel, AbstractParams):
    limit: int = Query(20, ge=1, le=100, description="Page offset")
    order: str = Query(default="desc", description="Sort order")
    after: Optional[str] = Query(None, description="Page after")
    before: Optional[str] = Query(None, description="Page before")

    def to_raw_params(self) -> CursorRawParams:
        return CursorRawParams(cursor=None, size=self.limit, include_total=True)


class CommonPage(AbstractPage[ModelType], Generic[ModelType]):
    __params_type__ = CursorParams

    object: str = "list"
    data: List[ModelType] = []
    first_id: Optional[str] = ""
    last_id: Optional[str] = ""
    has_more: bool = False

    @classmethod
    def create(
        cls,
        items: Sequence[ModelType],
        params: CursorParams,
        *,
        current: Optional[Cursor] = None,
        current_backwards: Optional[Cursor] = None,
        next_: Optional[Cursor] = None,
        previous: Optional[Cursor] = None,
        **kwargs: Any,
    ) -> AbstractPage[ModelType]:
        next_page = encode_cursor(next_)
        return create_pydantic_model(
            CommonPage,
            next_page=next_page,
            first_id=items[0].id if items else None,
            last_id=items[len(items) - 1].id if items else None,
            has_more=False if next_page is None else True,
            data=list(items),
        )


async def cursor_page(query: Any, db: AsyncSession) -> CommonPage[ModelType]:
    params, _ = verify_params(None, "cursor")
    model = query._propagate_attrs["plugin_subject"].class_

    logging.debug(
        f"Page model={model}, sort={params.order}, filter_parameters=before:{params.before}, after:{params.after}",
    )

    if params.before is not None:
        if params.order.upper() == "DESC":
            query = query.where(model.id > params.before)
        else:
            query = query.where(model.id < params.before)
    if params.after is not None:
        if params.order.upper() == "DESC":
            query = query.where(model.id < params.after)
        else:
            query = query.where(model.id > params.after)

    if params.order.upper() == "DESC":
        query = query.order_by(desc(model.__dict__["created_at"]))
    else:
        query = query.order_by(asc(model.__dict__["created_at"]))

    return await paginate(db, query)
