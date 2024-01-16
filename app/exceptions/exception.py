from typing import Any

from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    """
    基础异常
    """

    type: str = None
    param: str = None

    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str = None,
        type: str = None,
        param: str = None,
        detail: Any = None,
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.type = type
        self.param = param
        super().__init__(status_code, detail)

    def __str__(self) -> str:
        return f"status_code={self.status_code} error_code={self.error_code} message={self.message}"


class BadRequestError(BaseHTTPException):
    """
    请求参数异常
    """

    def __init__(self, message: str, error_code: str = "bad_request"):
        self.status_code = 400
        self.error_code = error_code
        self.message = message
        self.type = "invalid_request_error"


class ValidateFailedError(BaseHTTPException):
    """
    校验失败
    """

    def __init__(self, message: str = "Validation failed", error_code: str = "validation_failed"):
        self.status_code = 422
        self.error_code = error_code
        self.message = message
        self.type = error_code


class AuthenticationError(BaseHTTPException):
    """
    未认证
    """

    def __init__(self, message: str = "Unauthorized", error_code: str = "unauthorized"):
        self.status_code = 401
        self.error_code = error_code
        self.message = message


class AuthorizationError(BaseHTTPException):
    """
    未授权
    """

    def __init__(self, message: str = "Forbidden", error_code: str = "forbidden"):
        self.status_code = 403
        self.error_code = error_code
        self.message = message


class ResourceNotFoundError(BaseHTTPException):
    """
    资源不存在
    """

    def __init__(self, message: str = "Resource not found", error_code: str = "resource_not_found"):
        self.status_code = 404
        self.error_code = error_code
        self.message = message
        self.type = "not_found_error"


class InternalServerError(BaseHTTPException):
    """
    服务器内部异常
    """

    def __init__(self, message: str = "Internal Server Error", error_code: str = "internal_server_error"):
        self.status_code = 500
        self.message = message
        self.error_code = error_code
        self.type = error_code


class ServerError(BaseException):
    """
    服务端异常
    """

    def __init__(self, message: str):
        self.message = message
