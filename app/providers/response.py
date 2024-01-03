from fastapi.responses import JSONResponse


# class CustomJSONResponse(JSONResponse):
#
#     def render(self, data: any) -> bytes:
#         return json.dumps(
#             {'code': 'success', 'data': data},
#             ensure_ascii=False,
#             allow_nan=False,
#             indent=None,
#             separators=(",", ":"),
#         ).encode("utf-8")


class ErrorResponse(JSONResponse):
    def __init__(
        self, status_code: int, error_code: str, message: str = None, type_code: str = None, param: str = None
    ) -> None:
        super().__init__(
            status_code=status_code,
            # OpenAI style error response
            content={"error": {"code": error_code, "message": message, "type": type_code, "param": param}},
        )
