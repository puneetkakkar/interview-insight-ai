from unittest.mock import AsyncMock, MagicMock
from typing import Any, Dict

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


def mock_item_data() -> Dict[str, Any]:
    """Create mock item data for testing."""
    return {
        "id": 1,
        "title": "Test Item",
        "description": "Test Description",
        "price": 99.99,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "is_deleted": False,
        "deleted_at": None,
    }
