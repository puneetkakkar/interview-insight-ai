from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .crud_base import CRUDBase
from ..models.item import Item
from ..schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    """CRUD operations for Item model."""
    
    async def get_by_title(self, db: AsyncSession, *, title: str) -> Optional[Item]:
        """Get item by title."""
        result = await db.execute(
            select(Item).where(Item.title == title, Item.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    async def get_active_items(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Item]:
        """Get only active (non-deleted) items."""
        return await self.get_multi(
            db, 
            skip=skip, 
            limit=limit, 
            filters={"is_deleted": False}
        )
    
    async def search_by_title(
        self, 
        db: AsyncSession, 
        *, 
        title_search: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Item]:
        """Search items by title (partial match)."""
        result = await db.execute(
            select(Item)
            .where(Item.title.ilike(f"%{title_search}%"), Item.is_deleted == False)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


# Create CRUD instance
crud_items = CRUDItem(Item)
