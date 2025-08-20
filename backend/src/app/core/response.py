from typing import Any, Optional
from fastapi.encoders import jsonable_encoder


def build_success_response(data: Any, message: Optional[str] = None) -> dict[str, Any]:
    """Create a consistent success response envelope.

    Wrapped response for consistency; frontend checks 'success'.
    """
    payload: dict[str, Any] = {
        "success": True,
        "data": jsonable_encoder(data),
        "message": message,
    }
    # Remove message key if None to keep responses clean
    if message is None:
        payload.pop("message")
    return payload


def build_error_response(code: int, message: str, details: Any) -> dict[str, Any]:
    """Create a consistent error response envelope."""
    return {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "details": jsonable_encoder(details),
        },
    }


