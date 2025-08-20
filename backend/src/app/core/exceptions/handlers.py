from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from http import HTTPStatus

from ..logger import logger
from ..config import settings
from ..response import build_error_response


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    try:
        message = HTTPStatus(exc.status_code).phrase
    except ValueError:
        message = "HTTP Error"
    payload = build_error_response(
        code=exc.status_code,
        message=message,
        details=exc.detail,
    )
    logger.warning(
        "HTTPException: %s",
        exc.detail,
        extra={
            "request_id": getattr(getattr(request, "state", object()), "request_id", "-"),
            "path": request.url.path,
            "method": request.method,
            "status_code": exc.status_code,
        },
    )
    return JSONResponse(status_code=exc.status_code, content=payload)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    payload = build_error_response(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Validation Error",
        details=exc.errors(),
    )
    logger.warning(
        "Validation error",
        extra={
            "request_id": getattr(getattr(request, "state", object()), "request_id", "-"),
            "path": request.url.path,
            "method": request.method,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        },
    )
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=payload)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "Unhandled exception",
        extra={
            "request_id": getattr(getattr(request, "state", object()), "request_id", "-"),
            "path": request.url.path,
            "method": request.method,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
    )
    payload = build_error_response(
        code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Internal Server Error",
        details=str(exc) if settings.DEBUG else "Internal server error",
    )
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=payload)


