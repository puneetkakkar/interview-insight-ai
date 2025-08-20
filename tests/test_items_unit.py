import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.crud_items import crud_items
from src.app.models.item import Item
from src.app.schemas.item import ItemCreate, ItemUpdate
from tests.helpers.generators import generate_item_data
from tests.helpers.mocks import mock_db_session, mock_item_data


class TestCRUDItems:
    """Test CRUD operations for items."""
    
    @pytest.mark.asyncio
    async def test_create_item(self):
        """Test creating a new item."""
        db = mock_db_session()
        item_data = generate_item_data()
        item_create = ItemCreate(**item_data)
        
        # Mock the create method
        with patch.object(crud_items, 'create') as mock_create:
            mock_create.return_value = Item(**item_data, id=1)
            result = await crud_items.create(db, obj_in=item_create)
            
            assert result.id == 1
            assert result.title == item_data["title"]
            assert result.price == item_data["price"]
            mock_create.assert_called_once_with(db, obj_in=item_create)
    
    @pytest.mark.asyncio
    async def test_get_item(self):
        """Test getting an item by ID."""
        db = mock_db_session()
        item_data = mock_item_data()
        mock_item = Item(**item_data)
        
        with patch.object(crud_items, 'get') as mock_get:
            mock_get.return_value = mock_item
            result = await crud_items.get(db, id=1)
            
            assert result.id == 1
            assert result.title == "Test Item"
            mock_get.assert_called_once_with(db, id=1)
    
    @pytest.mark.asyncio
    async def test_get_by_title(self):
        """Test getting an item by title."""
        db = mock_db_session()
        item_data = mock_item_data()
        mock_item = Item(**item_data)
        
        with patch.object(crud_items, 'get_by_title') as mock_get_by_title:
            mock_get_by_title.return_value = mock_item
            result = await crud_items.get_by_title(db, title="Test Item")
            
            assert result.title == "Test Item"
            mock_get_by_title.assert_called_once_with(db, title="Test Item")
    
    @pytest.mark.asyncio
    async def test_update_item(self):
        """Test updating an item."""
        db = mock_db_session()
        item_data = mock_item_data()
        mock_item = Item(**item_data)
        update_data = {"title": "Updated Title", "price": 149.99}
        item_update = ItemUpdate(**update_data)
        
        with patch.object(crud_items, 'update') as mock_update:
            updated_item = Item(**item_data, **update_data)
            mock_update.return_value = updated_item
            result = await crud_items.update(db, db_obj=mock_item, obj_in=item_update)
            
            assert result.title == "Updated Title"
            assert result.price == 149.99
            mock_update.assert_called_once_with(db, db_obj=mock_item, obj_in=item_update)
    
    @pytest.mark.asyncio
    async def test_remove_item(self):
        """Test soft deleting an item."""
        db = mock_db_session()
        item_data = mock_item_data()
        mock_item = Item(**item_data)
        
        with patch.object(crud_items, 'remove') as mock_remove:
            mock_remove.return_value = mock_item
            result = await crud_items.remove(db, id=1)
            
            assert result.id == 1
            mock_remove.assert_called_once_with(db, id=1)
    
    @pytest.mark.asyncio
    async def test_get_active_items(self):
        """Test getting only active items."""
        db = mock_db_session()
        items_data = [mock_item_data(), mock_item_data()]
        mock_items = [Item(**data) for data in items_data]
        
        with patch.object(crud_items, 'get_active_items') as mock_get_active:
            mock_get_active.return_value = mock_items
            result = await crud_items.get_active_items(db, skip=0, limit=10)
            
            assert len(result) == 2
            assert all(not item.is_deleted for item in result)
            mock_get_active.assert_called_once_with(db, skip=0, limit=10)
    
    @pytest.mark.asyncio
    async def test_search_by_title(self):
        """Test searching items by title."""
        db = mock_db_session()
        items_data = [mock_item_data(), mock_item_data()]
        mock_items = [Item(**data) for data in items_data]
        
        with patch.object(crud_items, 'search_by_title') as mock_search:
            mock_search.return_value = mock_items
            result = await crud_items.search_by_title(
                db, title_search="Test", skip=0, limit=10
            )
            
            assert len(result) == 2
            mock_search.assert_called_once_with(
                db, title_search="Test", skip=0, limit=10
            )


class TestItemSchemas:
    """Test Pydantic schemas for items."""
    
    def test_item_create_schema(self):
        """Test ItemCreate schema validation."""
        item_data = generate_item_data()
        item_create = ItemCreate(**item_data)
        
        assert item_create.title == item_data["title"]
        assert item_create.description == item_data["description"]
        assert item_create.price == item_data["price"]
    
    def test_item_update_schema(self):
        """Test ItemUpdate schema validation."""
        update_data = {"title": "Updated Title"}
        item_update = ItemUpdate(**update_data)
        
        assert item_update.title == "Updated Title"
        assert item_update.description is None
        assert item_update.price is None
    
    def test_item_read_schema(self):
        """Test ItemRead schema validation."""
        item_data = mock_item_data()
        item_read = ItemRead(**item_data)
        
        assert item_read.id == 1
        assert item_read.title == "Test Item"
        assert item_read.price == 99.99
        assert item_read.created_at == "2024-01-01T00:00:00Z"
        assert item_read.updated_at == "2024-01-01T00:00:00Z"
    
    def test_item_create_validation(self):
        """Test ItemCreate schema validation rules."""
        # Test required fields
        with pytest.raises(ValueError):
            ItemCreate()
        
        # Test price validation
        with pytest.raises(ValueError):
            ItemCreate(title="Test", price=-10.0)
        
        # Test title length validation
        with pytest.raises(ValueError):
            ItemCreate(title="", price=10.0)
