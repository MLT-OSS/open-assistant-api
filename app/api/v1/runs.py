from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.api.deps import get_session
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
def list_runs(
    *,
    session: Session = Depends(get_session),
    thread_id: str,
):
    """
    Returns a list of runs belonging to a thread.
    """
    ThreadService.get_thread(session=session, thread_id=thread_id)
    return cursor_page(select(Run).where(Run.thread_id == thread_id), session)


@router.post(
    "/{thread_id}/runs",
    response_model=RunRead,
)
def create_run(
    *,
    session: Session = Depends(get_session),
    thread_id: str,
    body: RunCreate = ...,
) -> RunRead:
    """
    Create a run.
    """
    db_run = RunService.create_run(session=session, thread_id=thread_id, body=body)
    run_task.apply_async(args=(db_run.id,))
    return db_run


@router.get(
    "/{thread_id}/runs/{run_id}",
    response_model=RunRead,
)
def get_run(*, session: Session = Depends(get_session), thread_id: str, run_id: str = ...) -> RunRead:
    """
    Retrieves a run.
    """
    return RunService.get_run(session=session, run_id=run_id, thread_id=thread_id)


@router.post(
    "/{thread_id}/runs/{run_id}",
    response_model=RunRead,
)
def modify_run(
    *,
    session: Session = Depends(get_session),
    thread_id: str,
    run_id: str = ...,
    body: RunUpdate = ...,
) -> RunRead:
    """
    Modifies a run.
    """
    return RunService.modify_run(session=session, thread_id=thread_id, run_id=run_id, body=body)


@router.post(
    "/{thread_id}/runs/{run_id}/cancel",
    response_model=RunRead,
)
def cancel_run(*, session: Session = Depends(get_session), thread_id: str, run_id: str = ...) -> RunRead:
    """
    Cancels a run that is `in_progress`.
    """
    return RunService.cancel_run(session=session, thread_id=thread_id, run_id=run_id)


@router.get(
    "/{thread_id}/runs/{run_id}/steps",
    response_model=CommonPage[RunStep],
)
def list_run_steps(
    *,
    session: Session = Depends(get_session),
    thread_id: str,
    run_id: str = ...,
):
    """
    Returns a list of run steps belonging to a run.
    """
    return cursor_page(select(RunStep).where(RunStep.thread_id == thread_id).where(RunStep.run_id == run_id), session)


@router.get(
    "/{thread_id}/runs/{run_id}/steps/{step_id}",
    response_model=RunStep,
)
def get_run_step(
    *,
    session: Session = Depends(get_session),
    thread_id: str,
    run_id: str = ...,
    step_id: str = ...,
) -> RunStep:
    """
    Retrieves a run step.
    """
    return RunService.get_run_step(thread_id=thread_id, run_id=run_id, step_id=step_id, session=session)


@router.post(
    "/{thread_id}/runs/{run_id}/submit_tool_outputs",
    response_model=RunRead,
)
def submit_tool_ouputs_to_run(
    *,
    session: Session = Depends(get_session),
    thread_id: str,
    run_id: str = ...,
    body: SubmitToolOutputsRunRequest = ...,
) -> RunRead:
    """
    When a run has the `status: "requires_action"` and `required_action.type` is `submit_tool_outputs`,
    this endpoint can be used to submit the outputs from the tool calls once they're all completed.
    All outputs must be submitted in a single request.
    """
    db_run = RunService.submit_tool_ouputs_to_run(session=session, thread_id=thread_id, run_id=run_id, body=body)
    # Resume async task
    if db_run.status == "queued":
        run_task.apply_async(args=(db_run.id,))
    return db_run


@router.post("/runs", response_model=RunRead)
def create_thread_and_run(*, session: Session = Depends(get_session), body: CreateThreadAndRun) -> RunRead:
    """
    Create a thread and run it in one request.
    """
    return RunService.create_thread_and_run(session=session, body=body)
