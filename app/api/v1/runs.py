from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from starlette.responses import StreamingResponse

from app.api.deps import get_async_session
from app.core.runner import pub_handler
from app.exceptions.exception import ResourceNotFoundError, InternalServerError
from app.models import RunStep
from app.libs.paginate import cursor_page, CommonPage
from app.models.run import RunCreate, RunRead, RunUpdate, Run
from app.schemas.runs import SubmitToolOutputsRunRequest
from app.schemas.threads import CreateThreadAndRun
from app.services.run.run import RunService
from app.services.thread.thread import ThreadService
from app.tasks.run_task import run_task

router = APIRouter()


@router.get(
    "/{thread_id}/runs",
    response_model=CommonPage[Run],
)
async def list_runs(
    *,
    session: AsyncSession = Depends(get_async_session),
    thread_id: str,
):
    """
    Returns a list of runs belonging to a thread.
    """
    await ThreadService.get_thread(session=session, thread_id=thread_id)
    return await cursor_page(select(Run).where(Run.thread_id == thread_id), session)


@router.post(
    "/{thread_id}/runs",
    response_model=RunRead,
)
async def create_run(
    *,
    session: AsyncSession = Depends(get_async_session),
    thread_id: str,
    body: RunCreate = ...,
) -> RunRead:
    """
    Create a run.
    """
    db_run = await RunService.create_run(session=session, thread_id=thread_id, body=body)
    run_task.apply_async(args=(db_run.id,))
    return db_run


@router.get(
    "/{thread_id}/runs/{run_id}",
    response_model=RunRead,
)
async def get_run(*, session: AsyncSession = Depends(get_async_session), thread_id: str, run_id: str = ...) -> RunRead:
    """
    Retrieves a run.
    """
    return await RunService.get_run(session=session, run_id=run_id, thread_id=thread_id)


@router.post(
    "/{thread_id}/runs/{run_id}",
    response_model=RunRead,
)
async def modify_run(
    *,
    session: AsyncSession = Depends(get_async_session),
    thread_id: str,
    run_id: str = ...,
    body: RunUpdate = ...,
) -> RunRead:
    """
    Modifies a run.
    """
    return await RunService.modify_run(session=session, thread_id=thread_id, run_id=run_id, body=body)


@router.post(
    "/{thread_id}/runs/{run_id}/cancel",
    response_model=RunRead,
)
async def cancel_run(
    *, session: AsyncSession = Depends(get_async_session), thread_id: str, run_id: str = ...
) -> RunRead:
    """
    Cancels a run that is `in_progress`.
    """
    return await RunService.cancel_run(session=session, thread_id=thread_id, run_id=run_id)


@router.get(
    "/{thread_id}/runs/{run_id}/steps",
    response_model=CommonPage[RunStep],
)
async def list_run_steps(
    *,
    session: AsyncSession = Depends(get_async_session),
    thread_id: str,
    run_id: str = ...,
):
    """
    Returns a list of run steps belonging to a run.
    """
    return await cursor_page(
        select(RunStep).where(RunStep.thread_id == thread_id).where(RunStep.run_id == run_id), session
    )


@router.get(
    "/{thread_id}/runs/{run_id}/steps/{step_id}",
    response_model=RunStep,
)
async def get_run_step(
    *,
    session: AsyncSession = Depends(get_async_session),
    thread_id: str,
    run_id: str = ...,
    step_id: str = ...,
) -> RunStep:
    """
    Retrieves a run step.
    """
    return await RunService.get_run_step(thread_id=thread_id, run_id=run_id, step_id=step_id, session=session)


@router.post(
    "/{thread_id}/runs/{run_id}/submit_tool_outputs",
    response_model=RunRead,
)
async def submit_tool_outputs_to_run(
    *,
    session: AsyncSession = Depends(get_async_session),
    thread_id: str,
    run_id: str = ...,
    body: SubmitToolOutputsRunRequest = ...,
) -> RunRead:
    """
    When a run has the `status: "requires_action"` and `required_action.type` is `submit_tool_outputs`,
    this endpoint can be used to submit the outputs from the tool calls once they're all completed.
    All outputs must be submitted in a single request.
    """
    db_run = await RunService.submit_tool_outputs_to_run(session=session, thread_id=thread_id, run_id=run_id, body=body)
    # Resume async task
    if db_run.status == "queued":
        run_task.apply_async(args=(db_run.id,))
    return db_run


@router.post("/runs", response_model=RunRead)
async def create_thread_and_run(
    *, session: AsyncSession = Depends(get_async_session), body: CreateThreadAndRun
) -> RunRead:
    """
    Create a thread and run it in one request.
    """
    return await RunService.create_thread_and_run(session=session, body=body)


@router.get("/{thread_id}/runs/{run_id}/stream")
async def sub_stream(*, thread_id: str, run_id: str = ..., request: Request):
    """
    Subscription chat response stream
    """

    channel = pub_handler.generate_channel_name(run_id)

    def _to_output_data(data):
        return f"data: {data}\n\n"

    async def _stream():
        x_index = None
        while True:
            if await request.is_disconnected():
                break

            if not pub_handler.channel_exist(channel):
                raise ResourceNotFoundError()

            x_index, event = pub_handler.read_event(channel, x_index)
            if not event:
                break

            if event["type"] == "error":
                raise InternalServerError()

            if event["type"] == "end":
                break

            yield _to_output_data(event["data"])

        yield _to_output_data("[DONE]")

    return StreamingResponse(_stream(), media_type="text/event-stream")
