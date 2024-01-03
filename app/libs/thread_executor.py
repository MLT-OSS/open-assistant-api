import atexit
from concurrent.futures import Executor, ThreadPoolExecutor
import concurrent
import concurrent.futures

from typing import List


def get_executor_for_config(worker_num: int, thread_name_prefix: str) -> Executor:
    """
    Returns a generator that yields a ThreadPoolExecutor with the specified number of workers.

    Args:
        worker_num (int): The number of worker threads in the ThreadPoolExecutor.
        thread_name_prefix (str): thread name perfix.

    Yields:
        Executor: A ThreadPoolExecutor instance.

    """
    executor = ThreadPoolExecutor(max_workers=worker_num, thread_name_prefix=thread_name_prefix)
    atexit.register(executor.shutdown, wait=False)
    return executor


def run_with_executor(executor: Executor, func, tasks: List, timeout: int):
    """
    Executes the given function with the provided executor and tasks.

    Args:
        executor (Executor): The executor to use for running the tasks.
        func: The function to be executed.
        tasks (List): The list of tasks to be executed.
        timeout (int): The maximum time to wait for the tasks to complete.

    Returns:
        List: The results of the executed tasks.

    Raises:
        Exception: If any of the tasks raise an exception.
    """
    futures = [executor.submit(lambda args: func(*args), task) for task in tasks]
    done, _ = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_EXCEPTION, timeout=timeout)

    results = []
    for future in done:
        if future.exception():
            raise future.exception()

        if future.done():
            results.append(future.result())
    return results
