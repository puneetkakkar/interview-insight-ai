from typing import List, Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_db
from ...core.exceptions.http_exceptions import NotFoundException, DuplicateValueException
from ...repositories.items import items_repository
from ...schemas.item import ItemCreate, ItemRead, ItemUpdate
from ...core.response import build_success_response

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
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
    existing_item = await items_repository.get_by_title(db, title=item.title)
    if existing_item:
        raise DuplicateValueException(f"Item with title '{item.title}' already exists")
    
    created = await items_repository.create(db, obj_in=item)
    return build_success_response(created, message="Item created successfully")


@router.get("/")
async def read_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"),
    search: str = Query(None, description="Search items by title"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
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
        items = await items_repository.search_by_title(db, title_search=search, skip=skip, limit=limit)
    else:
        items = await items_repository.get_active_items(db, skip=skip, limit=limit)
    
    return build_success_response(items)


@router.get("/{item_id}")
async def read_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
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
    item = await items_repository.get(db, id=item_id)
    if not item or item.is_deleted:
        raise NotFoundException(f"Item with ID {item_id} not found")
    
    return build_success_response(item)


@router.put("/{item_id}")
async def update_item(
    item_id: int,
    item: ItemUpdate,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
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
    db_item = await items_repository.get(db, id=item_id)
    if not db_item or db_item.is_deleted:
        raise NotFoundException(f"Item with ID {item_id} not found")
    
    # Check for title conflicts if title is being updated
    if item.title and item.title != db_item.title:
        existing_item = await items_repository.get_by_title(db, title=item.title)
        if existing_item:
            raise DuplicateValueException(f"Item with title '{item.title}' already exists")
    
    # Update item
    updated_item = await items_repository.update(db, db_obj=db_item, obj_in=item)
    return build_success_response(updated_item, message="Item updated successfully")


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Soft delete an item.
    
    Args:
        item_id: Item ID
        db: Database session
        
    Raises:
        NotFoundException: If item not found
    """
    # Check if item exists
    db_item = await items_repository.get(db, id=item_id)
    if not db_item or db_item.is_deleted:
        raise NotFoundException(f"Item with ID {item_id} not found")
    
    # Soft delete
    await items_repository.remove(db, id=item_id)
    return build_success_response({"id": item_id}, message="Item deleted successfully")


@router.get("/search/{title_search}")
async def search_items(
    title_search: str,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
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
    items = await items_repository.search_by_title(
        db, 
        title_search=title_search, 
        skip=skip, 
        limit=limit
    )
    return build_success_response(items)
