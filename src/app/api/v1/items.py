from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_db
from ...core.exceptions.http_exceptions import NotFoundException, DuplicateValueException
from ...crud.crud_items import crud_items
from ...schemas.item import ItemCreate, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db)
) -> ItemRead:
    """
    Create a new item.
    
    Args:
        item: Item data to create
        db: Database session
        
    Returns:
        Created item data
        
    Raises:
        DuplicateValueException: If item with same title already exists
    """
    # Check if item with same title already exists
    existing_item = await crud_items.get_by_title(db, title=item.title)
    if existing_item:
        raise DuplicateValueException(f"Item with title '{item.title}' already exists")
    
    return await crud_items.create(db, obj_in=item)


@router.get("/", response_model=List[ItemRead])
async def read_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"),
    search: str = Query(None, description="Search items by title"),
    db: AsyncSession = Depends(get_db)
) -> List[ItemRead]:
    """
    Retrieve items with optional pagination and search.
    
    Args:
        skip: Number of items to skip for pagination
        limit: Maximum number of items to return
        search: Optional search term for title
        db: Database session
        
    Returns:
        List of items
    """
    if search:
        items = await crud_items.search_by_title(db, title_search=search, skip=skip, limit=limit)
    else:
        items = await crud_items.get_active_items(db, skip=skip, limit=limit)
    
    return items


@router.get("/{item_id}", response_model=ItemRead)
async def read_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
) -> ItemRead:
    """
    Retrieve a specific item by ID.
    
    Args:
        item_id: Item ID
        db: Database session
        
    Returns:
        Item data
        
    Raises:
        NotFoundException: If item not found
    """
    item = await crud_items.get(db, id=item_id)
    if not item or item.is_deleted:
        raise NotFoundException(f"Item with ID {item_id} not found")
    
    return item


@router.put("/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: int,
    item: ItemUpdate,
    db: AsyncSession = Depends(get_db)
) -> ItemRead:
    """
    Update an existing item.
    
    Args:
        item_id: Item ID
        item: Updated item data
        db: Database session
        
    Returns:
        Updated item data
        
    Raises:
        NotFoundException: If item not found
        DuplicateValueException: If new title conflicts with existing item
    """
    # Check if item exists
    db_item = await crud_items.get(db, id=item_id)
    if not db_item or db_item.is_deleted:
        raise NotFoundException(f"Item with ID {item_id} not found")
    
    # Check for title conflicts if title is being updated
    if item.title and item.title != db_item.title:
        existing_item = await crud_items.get_by_title(db, title=item.title)
        if existing_item:
            raise DuplicateValueException(f"Item with title '{item.title}' already exists")
    
    # Update item
    updated_item = await crud_items.update(db, db_obj=db_item, obj_in=item)
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Soft delete an item.
    
    Args:
        item_id: Item ID
        db: Database session
        
    Raises:
        NotFoundException: If item not found
    """
    # Check if item exists
    db_item = await crud_items.get(db, id=item_id)
    if not db_item or db_item.is_deleted:
        raise NotFoundException(f"Item with ID {item_id} not found")
    
    # Soft delete
    await crud_items.remove(db, id=item_id)


@router.get("/search/{title_search}", response_model=List[ItemRead])
async def search_items(
    title_search: str,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"),
    db: AsyncSession = Depends(get_db)
) -> List[ItemRead]:
    """
    Search items by title (partial match).
    
    Args:
        title_search: Search term for title
        skip: Number of items to skip for pagination
        limit: Maximum number of items to return
        db: Database session
        
    Returns:
        List of matching items
    """
    items = await crud_items.search_by_title(
        db, 
        title_search=title_search, 
        skip=skip, 
        limit=limit
    )
    return items
