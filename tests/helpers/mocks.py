from unittest.mock import AsyncMock, MagicMock
from typing import Any, Dict, List
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession


def mock_db_session() -> AsyncSession:
    """Create a mock database session for testing."""
    session = AsyncMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    session.refresh = AsyncMock()
    session.add = MagicMock()
    session.execute = AsyncMock()
    return session


def mock_item_data(overrides: Dict[str, Any] = None) -> Dict[str, Any]:
    """Create mock item data for testing."""
    data = {
        "id": 1,
        "title": "Test Item",
        "description": "Test Description",
        "price": 99.99,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "is_deleted": False,
        "deleted_at": None,
    }
    
    if overrides:
        data.update(overrides)
    
    return data


def mock_items_batch(count: int = 5, overrides: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """Create a batch of mock items for testing."""
    items = []
    for i in range(count):
        item_data = mock_item_data(overrides)
        item_data["id"] = i + 1
        item_data["title"] = f"Test Item {i + 1}"
        items.append(item_data)
    return items


def mock_deleted_item_data() -> Dict[str, Any]:
    """Create mock deleted item data for testing."""
    return mock_item_data({
        "is_deleted": True,
        "deleted_at": "2024-01-02T00:00:00Z",
    })


def mock_duplicate_item_data() -> Dict[str, Any]:
    """Create mock duplicate item data for testing."""
    return mock_item_data({
        "id": 2,
        "title": "Test Item",  # Same title as item 1
    })


def mock_updated_item_data() -> Dict[str, Any]:
    """Create mock updated item data for testing."""
    return mock_item_data({
        "title": "Updated Test Item",
        "price": 149.99,
        "updated_at": "2024-01-02T00:00:00Z",
    })


def mock_pagination_response(total: int = 100, page_size: int = 10) -> Dict[str, Any]:
    """Create mock pagination response data."""
    return {
        "items": mock_items_batch(page_size),
        "total": total,
        "page": 1,
        "pages": (total + page_size - 1) // page_size,
        "has_next": total > page_size,
        "has_prev": False,
    }


def mock_search_response(query: str, results: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create mock search response data."""
    if results is None:
        results = mock_items_batch(3)
    
    return {
        "query": query,
        "results": results,
        "total_results": len(results),
        "search_time_ms": 15,
    }


def mock_error_response(status_code: int = 400, message: str = "Bad Request") -> Dict[str, Any]:
    """Create mock error response data."""
    return {
        "success": False,
        "data": None,
        "error": {
            "code": status_code,
            "message": message,
            "details": f"Error details for {message}",
        },
    }


def mock_success_response(data: Any = None, message: str = None) -> Dict[str, Any]:
    """Create mock success response data."""
    response = {
        "success": True,
        "data": data or mock_item_data(),
    }
    
    if message:
        response["message"] = message
    
    return response
