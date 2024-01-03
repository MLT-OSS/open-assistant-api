import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.exception import AuthenticationError, AuthorizationError, BaseHTTPException
from app.providers.response import ErrorResponse


def register(app):
    @app.exception_handler(AuthenticationError)
    async def authentication_exception_handler(request: Request, e: AuthenticationError):
        """
        认证异常处理
        """
        return ErrorResponse(e.status_code, e.error_code, e.message)

    @app.exception_handler(AuthorizationError)
    async def authorization_exception_handler(request: Request, e: AuthorizationError):
        """
        权限异常处理
        """
        return ErrorResponse(e.status_code, e.error_code, e.message)

    @app.exception_handler(BaseHTTPException)
    async def business_exception_handler(request: Request, e: BaseHTTPException):
        """
        其他业务异常
        """
        logging.exception(e)
        return ErrorResponse(e.status_code, e.error_code, e.message, e.type, e.param)

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, e: StarletteHTTPException):
        logging.exception(e)
        return ErrorResponse(e.status_code, "http_error", e.detail)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, e: RequestValidationError):
        logging.exception(e)
        return ErrorResponse(422, "request_validation_error", str(e))
