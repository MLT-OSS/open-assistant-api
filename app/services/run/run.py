from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session, select, desc, update

from app.exceptions.exception import BadRequestError, ResourceNotFoundError, ValidateFailedError
from app.models import RunStep
from app.models.run import Run, RunRead, RunCreate, RunUpdate
from app.schemas.runs import SubmitToolOutputsRunRequest
from app.schemas.threads import CreateThreadAndRun
from app.services.assistant.assistant import AssistantService
from app.services.thread.thread import ThreadService


class RunService:
    @staticmethod
    def create_run(
        *,
        session: Session,
        thread_id: str,
        body: RunCreate = ...,
    ) -> RunRead:
        # get thread
        ThreadService.get_thread(session=session, thread_id=thread_id)
        # get assistant
        db_asst = AssistantService.get_assistant(session=session, assistant_id=body.assistant_id)
        if not body.model and db_asst.model:
            body.model = db_asst.model
        if not body.instructions and db_asst.instructions:
            body.instructions = db_asst.instructions
        if not body.tools and db_asst.tools:
            body.tools = db_asst.tools
        if not body.extra_body and db_asst.extra_body:
            body.extra_body = db_asst.extra_body
        # create run
        db_run = Run.model_validate(body.model_dump(), update={"thread_id": thread_id, "file_ids": db_asst.file_ids})
        session.add(db_run)
        session.commit()
        session.refresh(db_run)
        return db_run

    @staticmethod
    def modify_run(
        *,
        session: Session,
        thread_id: str,
        run_id: str,
        body: RunUpdate = ...,
    ) -> RunRead:
        ThreadService.get_thread(session=session, thread_id=thread_id)
        old_run = RunService.get_run(session=session, run_id=run_id)
        update_data = body.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(old_run, key, value)
        session.add(old_run)
        session.commit()
        session.refresh(old_run)
        return old_run

    @staticmethod
    def create_thread_and_run(
        *,
        session: Session,
        body: CreateThreadAndRun = ...,
    ) -> RunRead:
        # get assistant
        db_asst = AssistantService.get_assistant(session=session, assistant_id=body.assistant_id)
        # create thread
        thread_id = None
        if body.thread is not None:
            db_thread = ThreadService.create_thread(session=session, body=body.thread)
            thread_id = db_thread.id
        if body.model is None and db_asst.model is not None:
            body.model = db_asst.model
        if body.instructions is None and db_asst.instructions is not None:
            body.instructions = db_asst.instructions
        if body.tools is None and db_asst.tools is not None:
            body.tools = db_asst.tools
        # create run
        db_run = Run.model_validate(body, update={"thread_id": thread_id, "file_ids": db_asst.file_ids})
        session.add(db_run)
        session.commit()
        session.refresh(db_run)
        return db_run

    @staticmethod
    def cancel_run(
        *,
        session: Session,
        thread_id: str,
        run_id: str,
    ) -> RunRead:
        ThreadService.get_thread(session=session, thread_id=thread_id)
        db_run = RunService.get_run(session=session, run_id=run_id)
        # 判断任务状态
        if db_run.status == "cancelling":
            raise BadRequestError(message=f"run {run_id} already cancel")
        if db_run.status != "in_progress":
            raise BadRequestError(message=f"run {run_id} cannot cancel")
        db_run.status = "cancelling"
        db_run.cancelled_at = datetime.now()
        session.add(db_run)
        session.commit()
        session.refresh(db_run)
        return db_run

    @staticmethod
    def submit_tool_outputs_to_run(
        *, session: Session, thread_id, run_id, body: SubmitToolOutputsRunRequest
    ) -> RunRead:
        # get run
        db_run = RunService.get_run(session=session, run_id=run_id, thread_id=thread_id)
        # get run_step
        db_run_step = RunService.get_in_progress_run_step(run_id=run_id, session=session)
        if db_run.status != "requires_action":
            raise BadRequestError(message=f'Run status is "${db_run.status}", cannot submit tool outputs')
        # For now, this is always submit_tool_outputs.
        if not db_run.required_action or db_run.required_action["type"] != "submit_tool_outputs":
            raise HTTPException(
                status_code=500,
                detail=f'Run status is "${db_run.status}", but "run.required_action.type" is not '
                f'"submit_tool_outputs"',
            )

        tool_calls = db_run_step.step_details["tool_calls"]
        if not tool_calls:
            raise HTTPException(status_code=500, detail="Invalid tool call")

        for tool_output in body.tool_outputs:
            tool_call = next((t for t in tool_calls if t["id"] == tool_output.tool_call_id), None)
            if not tool_call:
                raise HTTPException(status_code=500, detail="Invalid tool call")
            if tool_call["type"] != "function":
                raise HTTPException(status_code=500, detail="Invalid tool call type")
            tool_call["function"]["output"] = tool_output.output

        # update
        step_completed = not list(filter(lambda tool_call: "output" not in tool_call[tool_call["type"]], tool_calls))
        if step_completed:
            stmt = (
                update(RunStep)
                .where(RunStep.id == db_run_step.id)
                .values({"status": "completed", "step_details": {"type": "tool_calls", "tool_calls": tool_calls}})
            )
        else:
            stmt = (
                update(RunStep)
                .where(RunStep.id == db_run_step.id)
                .values({"step_details": {"type": "tool_calls", "tool_calls": tool_calls}})
            )

        session.exec(stmt)

        tool_call_ids = [tool_output.tool_call_id for tool_output in body.tool_outputs]
        required_action_tool_calls = db_run.required_action["submit_tool_outputs"]["tool_calls"]
        required_action_tool_calls = list(
            filter(lambda tool_call: tool_call["id"] not in tool_call_ids, required_action_tool_calls)
        )

        required_action = {**db_run.required_action}
        if required_action_tool_calls:
            required_action["submit_tool_outputs"]["tool_calls"] = required_action_tool_calls
        else:
            required_action = {}

        if not required_action:
            stmt = (
                update(Run).where(Run.id == db_run.id).values({"required_action": required_action, "status": "queued"})
            )
        else:
            stmt = update(Run).where(Run.id == db_run.id).values({"required_action": required_action})

        session.exec(stmt)
        session.commit()
        session.refresh(db_run)
        return db_run

    @staticmethod
    def get_in_progress_run_step(*, run_id, session: Session) -> RunStep:
        run_step = session.exec(
            select(RunStep)
            .where(RunStep.run_id == run_id)
            .where(RunStep.type == "tool_calls")
            .where(RunStep.status == "in_progress")
            .order_by(desc(RunStep.created_at))
        ).one_or_none()
        if not run_step:
            raise ResourceNotFoundError("run_step not found or not in progress")
        return run_step

    @staticmethod
    def get_run(*, session: Session, run_id, thread_id=None) -> RunRead:
        statement = select(Run).where(Run.id == run_id)
        if thread_id is not None:
            statement = statement.where(Run.thread_id == thread_id)

        run = session.exec(statement).one_or_none()
        if not run:
            raise ResourceNotFoundError(f"run {run_id} not found")

        return run

    @staticmethod
    def get_run_step(*, thread_id, run_id, step_id, session: Session) -> RunStep:
        run_step = session.exec(
            select(RunStep)
            .where(RunStep.thread_id == thread_id, RunStep.run_id == run_id, RunStep.id == step_id)
            .order_by(desc(RunStep.created_at))
        ).one_or_none()
        if not run_step:
            raise ResourceNotFoundError("run_step not found")
        return run_step

    @staticmethod
    def to_queued(*, session: Session, run_id) -> Run:
        run = RunService.get_run(run_id=run_id, session=session)
        RunService.check_cancel_and_expire_status(run=run, session=session)
        RunService.check_status_in(run=run, status_list=["requires_action", "in_progress", "queued"])

        if run.status != "queued":
            run.status = "queued"
            session.add(run)
            session.commit()
            session.refresh(run)

        return run

    @staticmethod
    def to_in_progress(*, session: Session, run_id) -> Run:
        run = RunService.get_run(run_id=run_id, session=session)
        RunService.check_cancel_and_expire_status(run=run, session=session)
        RunService.check_status_in(run=run, status_list=["queued", "in_progress"])

        if run.status != "in_progress":
            run.status = "in_progress"
            run.started_at = run.started_at or datetime.now()
            run.required_action = None
            session.add(run)
            session.commit()
            session.refresh(run)

        return run

    @staticmethod
    def to_requires_action(*, session: Session, run_id, required_action) -> Run:
        run = RunService.get_run(run_id=run_id, session=session)
        RunService.check_cancel_and_expire_status(run=run, session=session)
        RunService.check_status_in(run=run, status_list=["in_progress", "requires_action"])

        if run.status != "requires_action":
            run.status = "requires_action"
            run.required_action = required_action
            session.add(run)
            session.commit()
            session.refresh(run)

        return run

    @staticmethod
    def to_cancelling(*, session: Session, run_id) -> Run:
        run = RunService.get_run(run_id=run_id, session=session)
        RunService.check_status_in(run=run, status_list=["in_progress", "cancelling"])

        if run.status != "cancelling":
            run.status = "cancelling"
            session.add(run)
            session.commit()
            session.refresh(run)

        return run

    @staticmethod
    def to_completed(*, session: Session, run_id) -> Run:
        run = RunService.get_run(run_id=run_id, session=session)
        RunService.check_cancel_and_expire_status(run=run, session=session)
        RunService.check_status_in(run=run, status_list=["in_progress", "completed"])

        if run.status != "completed":
            run.status = "completed"
            run.completed_at = datetime.now()
            session.add(run)
            session.commit()
            session.refresh(run)

        return run

    @staticmethod
    def to_failed(*, session: Session, run_id, last_error) -> Run:
        run = RunService.get_run(run_id=run_id, session=session)
        RunService.check_cancel_and_expire_status(run=run, session=session)
        RunService.check_status_in(run=run, status_list=["in_progress", "failed"])

        if run.status != "failed":
            run.status = "failed"
            run.failed_at = datetime.now()
            run.last_error = {"code": "server_error", "message": str(last_error)}
            session.add(run)
            session.commit()
            session.refresh(run)

        return run

    @staticmethod
    def check_status_in(run, status_list):
        if run.status not in status_list:
            raise ValidateFailedError(f"invalid run {run.id} status {run.status}")

    @staticmethod
    def check_cancel_and_expire_status(*, session: Session, run):
        if run.status == "cancelling":
            run.status = "cancelled"
            run.cancelled_at = datetime.now()
            session.add(run)
            session.commit()
            session.refresh(run)

        if run.status == "cancelled":
            raise ValidateFailedError(f"run {run.id} cancelled")

        now = datetime.now()
        if run.expires_at and run.expires_at < now:
            run.status = "expired"
            session.add(run)
            session.commit()
            session.refresh(run)
            raise ValidateFailedError(f"run {run.id} expired")
