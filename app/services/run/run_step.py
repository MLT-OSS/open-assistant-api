from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
from sqlmodel import select

from app.exceptions.exception import ResourceNotFoundError, ValidateFailedError
from app.models import RunStep


class RunStepService:
    @staticmethod
    def new_run_step(
        *, session: Session, type, status="in_progress", assistant_id, thread_id, run_id, step_details
    ) -> RunStep:
        run_step = RunStep(
            type=type,
            status=status,
            assistant_id=assistant_id,
            thread_id=thread_id,
            run_id=run_id,
            step_details=step_details,
        )

        session.add(run_step)
        session.commit()
        session.refresh(run_step)
        return run_step

    @staticmethod
    def get_run_step(*, run_step_id, session: Session) -> RunStep:
        run_step = session.execute(select(RunStep).where(RunStep.id == run_step_id)).scalars().one_or_none()
        if not run_step:
            raise ResourceNotFoundError(f"run_step {run_step_id} not found")

        return run_step

    @staticmethod
    def get_run_step_list(*, run_id, thread_id, session: Session) -> List[RunStep]:
        statement = select(RunStep).where(RunStep.run_id == run_id).where(RunStep.thread_id == thread_id)

        return session.execute(statement).scalars().all()

    @staticmethod
    def to_cancelled(*, session: Session, run_step_id) -> RunStep:
        run_step = RunStepService.get_run_step(run_step_id=run_step_id, session=session)
        RunStepService.check_status_in(run_step=run_step, status_list=["in_progress", "cancelled"])

        if run_step.status != "cancelled":
            run_step.status = "cancelled"
            run_step.cancelled_at = datetime.now()
            session.add(run_step)
            session.commit()
            session.refresh(run_step)

        return run_step

    @staticmethod
    def update_step_details(*, session: Session, run_step_id, step_details, completed=False) -> RunStep:
        run_step = RunStepService.get_run_step(run_step_id=run_step_id, session=session)
        RunStepService.check_status_in(run_step=run_step, status_list=["in_progress", "completed"])

        run_step.step_details = step_details

        if completed and run_step.status != "completed":
            run_step.status = "completed"
            run_step.completed_at = datetime.now()

        session.add(run_step)
        session.commit()
        session.refresh(run_step)

        return run_step

    @staticmethod
    def to_failed(*, session: Session, run_step_id, last_error) -> RunStep:
        run_step = RunStepService.get_run_step(run_step_id=run_step_id, session=session)
        RunStepService.check_status_in(run_step=run_step, status_list=["in_progress", "failed"])

        if run_step.status != "failed":
            run_step.status = "failed"
            run_step.failed_at = datetime.now()
            run_step.last_error = {"code": "server_error", "message": str(last_error)}
            session.add(run_step)
            session.commit()
            session.refresh(run_step)

        return run_step

    @staticmethod
    def check_status_in(run_step, status_list):
        if run_step.status not in status_list:
            raise ValidateFailedError(f"invalid run_step {run_step.id} status {run_step.status}")
