from collections.abc import AsyncGenerator
from typing import Union, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db.database import get_db as _get_db

# Database session dependency
async def get_db() -> AsyncGenerator[Union[AsyncSession, Any], None]:
    """Get database session dependency."""
    async for session in _get_db():
        yield session
