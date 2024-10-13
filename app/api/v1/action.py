from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

@router.get("", response_model=CommonPage[ActionRead])
async def list_actions(*, session: AsyncSession = Depends(get_async_session), token_id=Depends(get_token_id)):
    """
    Returns a list of Actions.
    """
    try:
        statement = auth_policy.token_filter(
            select(Action), field=Action.id, relation_type=RelationType.Action, token_id=token_id
        )
        page = await cursor_page(statement, session)
        page.data = [ast.model_dump(by_alias=True) for ast in page.data]
        return page.model_dump(by_alias=True)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("", response_model=List[ActionRead])
async def create_actions(
    *, session: AsyncSession = Depends(get_async_session), body: ActionBulkCreateRequest, token_id=Depends(get_token_id)
):
    """
    Create an action with openapi schema.
    """
    try:
        actions = await ActionService.create_actions(session=session, body=body, token_id=token_id)
        actions = [item.model_dump(by_alias=True) for item in actions]
        return actions
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{action_id}", response_model=ActionRead)
async def get_action(*, session: AsyncSession = Depends(get_async_session), action_id: str):
    """
    Retrieves an action.
    """
    try:
        action = await ActionService.get_action(session=session, action_id=action_id)
        return action.model_dump(by_alias=True)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{action_id}", response_model=ActionRead)
async def modify_action(
    *, session: AsyncSession = Depends(get_async_session), action_id: str, body: ActionUpdateRequest
):
    """
    Modifies an action.
    """
    try:
        action = await ActionService.modify_action(session=session, action_id=action_id, body=body)
        return action.model_dump(by_alias=True)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{action_id}", response_model=DeleteResponse)
async def delete_action(*, session: AsyncSession = Depends(get_async_session), action_id: str) -> DeleteResponse:
    """
    Delete an action.
    """
    try:
        return await ActionService.delete_action(session=session, action_id=action_id)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{action_id}/run",
    response_model=BaseSuccessDataResponse,
)
async def api_run_action(*, session: AsyncSession = Depends(get_async_session), action_id: str, body: ActionRunRequest):
    try:
        response: Dict = await ActionService.run_action(
            session=session,
            action_id=action_id,
            parameters=body.parameters,
            headers=body.headers,
        )
        return BaseSuccessDataResponse(data=response)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
