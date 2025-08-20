from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException

from ..logger import logger
from ..config import settings


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    payload = {
        "error": {
            "type": "http_error",
            "status_code": exc.status_code,
            "detail": exc.detail,
        }
    }
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
    payload = {
        "error": {
            "type": "validation_error",
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "detail": exc.errors(),
        }
    }
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
    payload = {
        "error": {
            "type": "internal_server_error",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": str(exc) if settings.DEBUG else "Internal server error",
        }
    }
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=payload)


