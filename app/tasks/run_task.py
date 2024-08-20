import datetime
import logging

from app.core.runner.pub_handler import StreamEventHandler
from app.core.runner.thread_runner import ThreadRunner
from app.providers.celery_app import celery_app
from app.providers.database import session
from app.services.run.run import RunService


@celery_app.task(bind=True, autoretry_for=())
def run_task(self, run_id: str, stream: bool = False):
    logging.info(f"[run_task] [{run_id}] running at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        ThreadRunner(run_id, session, stream).run()
    except Exception as e:
        logging.exception(e)
        StreamEventHandler(run_id=run_id, is_stream=True).pub_error(str(e))
        RunService.to_failed(session=session, run_id=run_id, last_error=e)
    finally:
        session.close()
