import datetime
import logging

from app.api.deps import get_session
from app.core.runner.thread_runner import ThreadRunner
from app.providers.celery_app import celery_app
from app.services.run.run import RunService


@celery_app.task(bind=True, autoretry_for=(Exception,), max_retries=3, default_retry_delay=5)
def run_task(self, run_id: str):
    logging.info(f"[run_task] [{run_id}] running at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        ThreadRunner(run_id).run()
    except Exception as e:
        logging.exception(e)

        if self.request.retries == self.max_retries:
            RunService.to_failed(session=next(get_session()), run_id=run_id, last_error=e)
        else:
            RunService.to_queued(session=next(get_session()), run_id=run_id)

        raise self.retry(exc=e)
