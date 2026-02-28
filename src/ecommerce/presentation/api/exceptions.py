from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.ecommerce.presentation.api.schemas import ErrorResponse, ErrorDetail

HTTP_STATUS_MAP = {
    400: "INVALID_ARGUMENT",
    401: "UNAUTHENTICATED",
    403: "PERMISSION_DENIED",
    404: "NOT_FOUND",
    409: "ALREADY_EXISTS",
    422: "INVALID_ARGUMENT",
    429: "RESOURCE_EXHAUSTED",
    500: "INTERNAL",
    503: "UNAVAILABLE",
}


def get_status_string(status_code: int) -> str:
    return HTTP_STATUS_MAP.get(status_code, "UNKNOWN")


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        error_response = ErrorResponse(
            error=ErrorDetail(
                code=exc.status_code,
                message=str(exc.detail),
                status=get_status_string(exc.status_code),
            )
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        details = [
            {
                "field": ".".join(str(loc) for loc in error["loc"]),
                "reason": error["msg"],
            }
            for error in exc.errors()
        ]
        error_response = ErrorResponse(
            error=ErrorDetail(
                code=422,
                message="Request validation failed",
                status="INVALID_ARGUMENT",
                details=details,
            )
        )
        return JSONResponse(
            status_code=422,
            content=error_response.model_dump(),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        error_response = ErrorResponse(
            error=ErrorDetail(
                code=500,
                message="Internal server error",
                status="INTERNAL",
            )
        )
        return JSONResponse(
            status_code=500,
            content=error_response.model_dump(),
        )
