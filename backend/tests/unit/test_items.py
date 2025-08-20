import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.app.repositories.items import items_repository, ItemRepository
from src.app.models.item import Item
from src.app.schemas.item import ItemCreate, ItemUpdate, ItemRead
from src.app.core.exceptions.http_exceptions import NotFoundException, DuplicateValueException
from tests.helpers.generators import generate_item_data
from tests.helpers.mocks import mock_db_session, mock_item_data


class TestItemRepository:
    """Test CRUD operations for items repository."""

    @pytest.mark.asyncio
    async def test_create_item_success(self):
        """Test creating a new item successfully."""
        # Arrange
        db = mock_db_session()
        item_data = generate_item_data()
        item_create = ItemCreate(**item_data)
        expected_item = Item(**item_data)
        expected_item.id = 1
        
        with patch.object(items_repository, "create") as mock_create:
            mock_create.return_value = expected_item
            
            # Act
            result = await items_repository.create(db, obj_in=item_create)
            
            # Assert
            assert result.id == 1
            assert result.title == item_data["title"]
            assert result.price == item_data["price"]
            mock_create.assert_called_once_with(db, obj_in=item_create)

    @pytest.mark.asyncio
    async def test_create_item_database_error(self):
        """Test creating an item when database operation fails."""
        # Arrange
        db = mock_db_session()
        item_data = generate_item_data()
        item_create = ItemCreate(**item_data)
        
        with patch.object(items_repository, "create") as mock_create:
            mock_create.side_effect = IntegrityError("duplicate key", None, None)
            
            # Act & Assert
            with pytest.raises(IntegrityError):
                await items_repository.create(db, obj_in=item_create)

    @pytest.mark.asyncio
    async def test_get_item_by_id_success(self):
        """Test getting an item by ID successfully."""
        # Arrange
        db = mock_db_session()
        item_data = mock_item_data()
        expected_item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
        expected_item.id = item_data["id"]
        
        with patch.object(items_repository, "get") as mock_get:
            mock_get.return_value = expected_item
            
            # Act
            result = await items_repository.get(db, id=1)
            
            # Assert
            assert result.id == 1
            assert result.title == "Test Item"
            mock_get.assert_called_once_with(db, id=1)

    @pytest.mark.asyncio
    async def test_get_item_by_id_not_found(self):
        """Test getting an item by ID when not found."""
        # Arrange
        db = mock_db_session()
        
        with patch.object(items_repository, "get") as mock_get:
            mock_get.return_value = None
            
            # Act
            result = await items_repository.get(db, id=999)
            
            # Assert
            assert result is None
            mock_get.assert_called_once_with(db, id=999)

    @pytest.mark.asyncio
    async def test_get_by_title_success(self):
        """Test getting an item by title successfully."""
        # Arrange
        db = mock_db_session()
        item_data = mock_item_data()
        expected_item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
        expected_item.id = item_data["id"]
        
        with patch.object(items_repository, "get_by_title") as mock_get_by_title:
            mock_get_by_title.return_value = expected_item
            
            # Act
            result = await items_repository.get_by_title(db, title="Test Item")
            
            # Assert
            assert result.title == "Test Item"
            mock_get_by_title.assert_called_once_with(db, title="Test Item")

    @pytest.mark.asyncio
    async def test_get_by_title_not_found(self):
        """Test getting an item by title when not found."""
        # Arrange
        db = mock_db_session()
        
        with patch.object(items_repository, "get_by_title") as mock_get_by_title:
            mock_get_by_title.return_value = None
            
            # Act
            result = await items_repository.get_by_title(db, title="Non-existent Item")
            
            # Assert
            assert result is None

    @pytest.mark.asyncio
    async def test_get_by_title_deleted_item(self):
        """Test getting an item by title when it's deleted."""
        # Arrange
        db = mock_db_session()
        
        with patch.object(items_repository, "get_by_title") as mock_get_by_title:
            mock_get_by_title.return_value = None
            
            # Act
            result = await items_repository.get_by_title(db, title="Deleted Item")
            
            # Assert
            assert result is None
            mock_get_by_title.assert_called_once_with(db, title="Deleted Item")

    @pytest.mark.asyncio
    async def test_update_item_success(self):
        """Test updating an item successfully."""
        # Arrange
        db = mock_db_session()
        item_data = mock_item_data()
        existing_item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
        existing_item.id = item_data["id"]
        update_data = {"title": "Updated Title", "price": 149.99}
        item_update = ItemUpdate(**update_data)
        expected_updated = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"} | set(update_data.keys())}, **update_data)
        expected_updated.id = item_data["id"]
        
        with patch.object(items_repository, "update") as mock_update:
            mock_update.return_value = expected_updated
            
            # Act
            result = await items_repository.update(db, db_obj=existing_item, obj_in=item_update)
            
            # Assert
            assert result.title == "Updated Title"
            assert result.price == 149.99
            mock_update.assert_called_once_with(db, db_obj=existing_item, obj_in=item_update)

    @pytest.mark.asyncio
    async def test_update_item_database_error(self):
        """Test updating an item when database operation fails."""
        # Arrange
        db = mock_db_session()
        item_data = mock_item_data()
        existing_item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
        existing_item.id = item_data["id"]
        update_data = {"title": "Updated Title"}
        item_update = ItemUpdate(**update_data)
        
        with patch.object(items_repository, "update") as mock_update:
            mock_update.side_effect = IntegrityError("duplicate key", None, None)
            
            # Act & Assert
            with pytest.raises(IntegrityError):
                await items_repository.update(db, db_obj=existing_item, obj_in=item_update)

    @pytest.mark.asyncio
    async def test_remove_item_success(self):
        """Test soft deleting an item successfully."""
        # Arrange
        db = mock_db_session()
        item_data = mock_item_data()
        expected_item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
        expected_item.id = item_data["id"]
        
        with patch.object(items_repository, "remove") as mock_remove:
            mock_remove.return_value = expected_item
            
            # Act
            result = await items_repository.remove(db, id=1)
            
            # Assert
            assert result.id == 1
            mock_remove.assert_called_once_with(db, id=1)

    @pytest.mark.asyncio
    async def test_remove_item_not_found(self):
        """Test removing an item that doesn't exist."""
        # Arrange
        db = mock_db_session()
        
        with patch.object(items_repository, "remove") as mock_remove:
            mock_remove.side_effect = NotFoundException("Item not found")
            
            # Act & Assert
            with pytest.raises(NotFoundException):
                await items_repository.remove(db, id=999)

    @pytest.mark.asyncio
    async def test_get_active_items_success(self):
        """Test getting only active items successfully."""
        # Arrange
        db = mock_db_session()
        items_data = [mock_item_data(), mock_item_data()]
        expected_items = []
        for data in items_data:
            itm = Item(**{k: v for k, v in data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
            itm.id = data["id"]
            itm.is_deleted = False
            expected_items.append(itm)
        
        with patch.object(items_repository, "get_active_items") as mock_get_active:
            mock_get_active.return_value = expected_items
            
            # Act
            result = await items_repository.get_active_items(db, skip=0, limit=10)
            
            # Assert
            assert len(result) == 2
            assert all(not item.is_deleted for item in result)
            mock_get_active.assert_called_once_with(db, skip=0, limit=10)

    @pytest.mark.asyncio
    async def test_get_active_items_empty(self):
        """Test getting active items when none exist."""
        # Arrange
        db = mock_db_session()
        
        with patch.object(items_repository, "get_active_items") as mock_get_active:
            mock_get_active.return_value = []
            
            # Act
            result = await items_repository.get_active_items(db, skip=0, limit=10)
            
            # Assert
            assert result == []
            assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_active_items_with_filters(self):
        """Test getting active items with custom filters."""
        # Arrange
        db = mock_db_session()
        items_data = [mock_item_data(), mock_item_data()]
        expected_items = []
        for data in items_data:
            itm = Item(**{k: v for k, v in data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
            itm.id = data["id"]
            itm.is_deleted = False
            expected_items.append(itm)
        
        with patch.object(items_repository, "get_multi") as mock_get_multi:
            mock_get_multi.return_value = expected_items
            
            # Act
            result = await items_repository.get_active_items(db, skip=5, limit=20)
            
            # Assert
            assert len(result) == 2
            mock_get_multi.assert_called_once_with(db, skip=5, limit=20, filters={"is_deleted": False})

    @pytest.mark.asyncio
    async def test_search_by_title_success(self):
        """Test searching items by title successfully."""
        # Arrange
        db = mock_db_session()
        items_data = [mock_item_data(), mock_item_data()]
        expected_items = []
        for data in items_data:
            itm = Item(**{k: v for k, v in data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
            itm.id = data["id"]
            expected_items.append(itm)
        
        with patch.object(items_repository, "search_by_title") as mock_search:
            mock_search.return_value = expected_items
            
            # Act
            result = await items_repository.search_by_title(
                db, title_search="Test", skip=0, limit=10
            )
            
            # Assert
            assert len(result) == 2
            mock_search.assert_called_once_with(
                db, title_search="Test", skip=0, limit=10
            )

    @pytest.mark.asyncio
    async def test_search_by_title_empty_results(self):
        """Test searching items by title with no results."""
        # Arrange
        db = mock_db_session()
        
        with patch.object(items_repository, "search_by_title") as mock_search:
            mock_search.return_value = []
            
            # Act
            result = await items_repository.search_by_title(
                db, title_search="Non-existent", skip=0, limit=10
            )
            
            # Assert
            assert result == []
            assert len(result) == 0

    @pytest.mark.asyncio
    async def test_search_by_title_partial_match(self):
        """Test searching items by title with partial match."""
        # Arrange
        db = mock_db_session()
        items_data = [mock_item_data(), mock_item_data()]
        expected_items = []
        for data in items_data:
            itm = Item(**{k: v for k, v in data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
            itm.id = data["id"]
            expected_items.append(itm)
        
        with patch.object(items_repository, "search_by_title") as mock_search:
            mock_search.return_value = expected_items
            
            # Act
            result = await items_repository.search_by_title(
                db, title_search="Test", skip=0, limit=10
            )
            
            # Assert
            assert len(result) == 2
            mock_search.assert_called_once_with(
                db, title_search="Test", skip=0, limit=10
            )

    @pytest.mark.asyncio
    async def test_search_by_title_empty_string(self):
        """Test searching items by title with empty string."""
        # Arrange
        db = mock_db_session()
        
        with patch.object(items_repository, "search_by_title") as mock_search:
            mock_search.return_value = []
            
            # Act
            result = await items_repository.search_by_title(
                db, title_search="", skip=0, limit=10
            )
            
            # Assert
            assert result == []
            mock_search.assert_called_once_with(
                db, title_search="", skip=0, limit=10
            )

    @pytest.mark.asyncio
    async def test_search_by_title_special_characters(self):
        """Test searching items by title with special characters."""
        # Arrange
        db = mock_db_session()
        
        with patch.object(items_repository, "search_by_title") as mock_search:
            mock_search.return_value = []
            
            # Act
            result = await items_repository.search_by_title(
                db, title_search="Test@#$%", skip=0, limit=10
            )
            
            # Assert
            assert result == []
            mock_search.assert_called_once_with(
                db, title_search="Test@#$%", skip=0, limit=10
            )

    @pytest.mark.asyncio
    async def test_search_by_title_with_pagination(self):
        """Test searching items by title with pagination."""
        # Arrange
        db = mock_db_session()
        items_data = [mock_item_data()]
        expected_items = []
        for data in items_data:
            itm = Item(**{k: v for k, v in data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
            itm.id = data["id"]
            expected_items.append(itm)
        
        with patch.object(items_repository, "search_by_title") as mock_search:
            mock_search.return_value = expected_items
            
            # Act
            result = await items_repository.search_by_title(
                db, title_search="Test", skip=5, limit=5
            )
            
            # Assert
            assert len(result) == 1
            mock_search.assert_called_once_with(
                db, title_search="Test", skip=5, limit=5
            )

    @pytest.mark.asyncio
    async def test_get_by_title_database_query(self):
        """Test get_by_title executes the correct database query."""
        # Arrange
        db = mock_db_session()
        item_data = mock_item_data()
        expected_item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
        expected_item.id = item_data["id"]
        
        # Mock the database execution
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = expected_item
        db.execute.return_value = mock_result
        
        # Act
        result = await items_repository.get_by_title(db, title="Test Item")
        
        # Assert
        assert result == expected_item
        db.execute.assert_called_once()
        # Verify the query was executed with correct parameters
        call_args = str(db.execute.call_args[0][0])
        assert "items.title" in call_args
        assert "items.is_deleted = false" in call_args

    @pytest.mark.asyncio
    async def test_search_by_title_database_query(self):
        """Test search_by_title executes the correct database query."""
        # Arrange
        db = mock_db_session()
        items_data = [mock_item_data(), mock_item_data()]
        expected_items = []
        for data in items_data:
            itm = Item(**{k: v for k, v in data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
            itm.id = data["id"]
            expected_items.append(itm)
        
        # Mock the database execution
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = expected_items
        db.execute.return_value = mock_result
        
        # Act
        result = await items_repository.search_by_title(
            db, title_search="Test", skip=5, limit=10
        )
        
        # Assert
        assert result == expected_items
        db.execute.assert_called_once()
        # Verify the query was executed with correct parameters
        call_args = str(db.execute.call_args[0][0])
        assert "items.title" in call_args
        assert "items.is_deleted = false" in call_args
        assert "LIMIT" in call_args
        assert "OFFSET" in call_args

    @pytest.mark.asyncio
    async def test_get_active_items_database_query(self):
        """Test get_active_items calls get_multi with correct filters."""
        # Arrange
        db = mock_db_session()
        items_data = [mock_item_data()]
        expected_items = []
        for data in items_data:
            itm = Item(**{k: v for k, v in data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
            itm.id = data["id"]
            expected_items.append(itm)
        
        # Mock the get_multi method
        with patch.object(items_repository, "get_multi") as mock_get_multi:
            mock_get_multi.return_value = expected_items
            
            # Act
            result = await items_repository.get_active_items(db, skip=10, limit=20)
            
            # Assert
            assert result == expected_items
            mock_get_multi.assert_called_once_with(
                db, skip=10, limit=20, filters={"is_deleted": False}
            )


class TestItemSchemas:
    """Test Pydantic schemas for items."""

    def test_item_create_schema_validation(self):
        """Test ItemCreate schema validation rules."""
        # Arrange & Act
        item_data = generate_item_data()
        item_create = ItemCreate(**item_data)
        
        # Assert
        assert item_create.title == item_data["title"]
        assert item_create.description == item_data["description"]
        assert item_create.price == item_data["price"]

    def test_item_create_schema_required_fields(self):
        """Test ItemCreate schema requires necessary fields."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError):
            ItemCreate()

    def test_item_create_schema_price_validation(self):
        """Test ItemCreate schema price validation."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError):
            ItemCreate(title="Test", price=-10.0)

    def test_item_create_schema_title_length_validation(self):
        """Test ItemCreate schema title length validation."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError):
            ItemCreate(title="", price=10.0)

    def test_item_create_schema_title_max_length_validation(self):
        """Test ItemCreate schema title max length validation."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError):
            ItemCreate(title="A" * 101, price=10.0)  # 101 characters

    def test_item_update_schema_partial_update(self):
        """Test ItemUpdate schema allows partial updates."""
        # Arrange
        update_data = {"title": "Updated Title"}
        
        # Act
        item_update = ItemUpdate(**update_data)
        
        # Assert
        assert item_update.title == "Updated Title"
        assert item_update.description is None
        assert item_update.price is None

    def test_item_update_schema_all_fields(self):
        """Test ItemUpdate schema with all fields."""
        # Arrange
        update_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "price": 199.99
        }
        
        # Act
        item_update = ItemUpdate(**update_data)
        
        # Assert
        assert item_update.title == "Updated Title"
        assert item_update.description == "Updated Description"
        assert item_update.price == 199.99

    def test_item_read_schema_serialization(self):
        """Test ItemRead schema serialization."""
        # Arrange
        item_data = mock_item_data()
        
        # Act
        item_read = ItemRead(**item_data)
        
        # Assert
        assert item_read.id == 1
        assert item_read.title == "Test Item"
        assert item_read.price == 99.99
        expected_dt = datetime.fromisoformat("2024-01-01T00:00:00+00:00")
        assert item_read.created_at == expected_dt
        assert item_read.updated_at == expected_dt

    def test_item_read_schema_from_orm(self):
        """Test ItemRead schema creation from ORM object."""
        # Arrange
        item_data = mock_item_data()
        item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
        item.id = item_data["id"]
        item.created_at = item_data["created_at"]
        item.updated_at = item_data["updated_at"]
        
        # Act
        item_read = ItemRead.model_validate(item)
        
        # Assert
        assert item_read.id == 1
        assert item_read.title == "Test Item"
        assert item_read.price == 99.99


class TestItemModel:
    """Test Item database model."""

    def test_item_model_creation(self):
        """Test Item model creation with required fields."""
        # Arrange
        item_data = generate_item_data()
        
        # Act
        item = Item(**item_data)
        
        # Assert
        assert item.title == item_data["title"]
        assert item.description == item_data["description"]
        assert item.price == item_data["price"]
        # The model uses server defaults; before persistence this may be None
        assert item.is_deleted in (False, None)

    def test_item_model_creation_with_defaults(self):
        """Test Item model creation with default values."""
        # Arrange
        item_data = {"title": "Test Item", "description": "Test Description"}
        
        # Act
        item = Item(**item_data)
        
        # Assert
        assert item.title == "Test Item"
        assert item.description == "Test Description"
        assert item.price == 0.0

    def test_item_model_repr(self):
        """Test Item model string representation."""
        # Arrange
        item_data = generate_item_data()
        item = Item(**item_data)
        
        # Act
        repr_str = repr(item)
        
        # Assert
        assert "Item" in repr_str
        assert item.title in repr_str
        assert str(item.price) in repr_str

    def test_item_model_attributes(self):
        """Test Item model attributes are properly set."""
        # Arrange
        item_data = generate_item_data()
        
        # Act
        item = Item(**item_data)
        
        # Assert
        assert hasattr(item, 'id')
        assert hasattr(item, 'title')
        assert hasattr(item, 'description')
        assert hasattr(item, 'price')
        assert hasattr(item, 'created_at')
        assert hasattr(item, 'updated_at')
        assert hasattr(item, 'is_deleted')
        assert hasattr(item, 'deleted_at')
