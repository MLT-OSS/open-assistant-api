import logging
from starlette.middleware.base import BaseHTTPMiddleware

from app.providers.response import ErrorResponse


# Bug: exception_handler unable to catch Exception
# https://github.com/tiangolo/fastapi/issues/4025
class UnhandledExceptionHandlingMiddleware(BaseHTTPMiddleware):
    """
    处理其他未知异常
    """

    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logging.exception(e)
            return ErrorResponse(500, "internal_server_error", "Internal Server Error")
