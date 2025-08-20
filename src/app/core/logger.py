import logging
import os
import sys
import time
import uuid
from typing import Any, Dict

from pythonjsonlogger import jsonlogger

try:
    from colorlog import ColoredFormatter
except Exception:  # pragma: no cover - optional in prod
    ColoredFormatter = None  # type: ignore

from .config import settings


def _get_console_formatter() -> logging.Formatter:
    if settings.DEBUG and ColoredFormatter is not None:
        return ColoredFormatter(
            fmt=(
                "%(log_color)s%(levelname)-8s%(reset)s | %(asctime)s | %(cyan)s%(name)s%(reset)s | "
                "%(method)s %(path)s -> %(status_code)s (%(duration_ms)sdms) [req:%(request_id)s] "
                "| %(message)s"
            ),
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "blue",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
    # Fallback plain formatter
    return logging.Formatter(
        fmt=(
            "%(levelname)-8s | %(asctime)s | %(name)s | "
            "%(method)s %(path)s -> %(status_code)s (%(duration_ms)sdms) [req:%(request_id)s] | %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _get_json_formatter() -> logging.Formatter:
    return jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s %(request_id)s %(path)s %(method)s %(status_code)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )


def setup_logger() -> logging.Logger:
    """Configure root app logger for dev/prod."""
    logger = logging.getLogger("fastapi-minimal")
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    if settings.DEBUG:
        console_handler.setFormatter(_get_console_formatter())
    else:
        console_handler.setFormatter(_get_json_formatter())

    logger.addHandler(console_handler)
    logger.propagate = False

    # Reduce verbosity from noisy libs in prod
    for noisy in ("uvicorn", "uvicorn.error", "uvicorn.access", "sqlalchemy.engine"):
        nl = logging.getLogger(noisy)
        nl.setLevel(logging.INFO if settings.DEBUG else logging.WARNING)

    return logger


# Global logger instance
logger = setup_logger()


class RequestContextFilter(logging.Filter):
    """Inject request_id if present in record's extra."""

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: D401
        # Provide safe defaults for fields used by formatters
        defaults: Dict[str, Any] = {
            "request_id": "-",
            "path": "-",
            "method": "-",
            "status_code": "-",
            "duration_ms": 0,
        }
        for key, value in defaults.items():
            if not hasattr(record, key):
                setattr(record, key, value)
        return True


logger.addFilter(RequestContextFilter())

