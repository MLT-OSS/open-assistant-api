import datetime
import logging

from app.core.runner.pub_handler import StreamEventHandler
from app.core.runner.thread_runner import ThreadRunner
from app.providers.celery_app import celery_app
from app.providers.database import session
from app.services.run.run import RunService


@celery_app.task(bind=True, autoretry_for=())
def run_task(self, run_id: str, stream: bool = False):
    """
    Celery task to run a job using ThreadRunner.
    
    Args:
        run_id (str): The unique identifier for the run.
        stream (bool): Flag to enable streaming of events. Default is False.
    """
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"[run_task] [{run_id}] running at {current_time}")

    try:
        # Execute the thread runner
        execute_runner(run_id, stream)
    except Exception as e:
        handle_exception(run_id, e)
    finally:
        close_session()


def execute_runner(run_id: str, stream: bool):
    """
    Initializes and runs the ThreadRunner.

    Args:
        run_id (str): The unique identifier for the run.
        stream (bool): Flag to enable streaming of events.
    """
    ThreadRunner(run_id, session, stream).run()


def handle_exception(run_id: str, exception: Exception):
    """
    Handles exceptions by logging and updating the run status.

    Args:
        run_id (str): The unique identifier for the run.
        exception (Exception): The exception to handle.
    """
    logging.exception(f"[run_task] [{run_id}] Error: {exception}")
    StreamEventHandler(run_id=run_id, is_stream=True).pub_error(str(exception))
    RunService.to_failed(session=session, run_id=run_id, last_error=exception)


def close_session():
    """
    Closes the database session.
    """
    try:
        session.close()
    except Exception as close_exception:
        logging.warning(f"Failed to close session: {close_exception}")
