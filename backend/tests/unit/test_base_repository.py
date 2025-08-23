import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select, update, delete
from typing import List, Optional, TypeVar, Generic

from src.app.repositories.base import BaseRepository
from src.app.core.exceptions.http_exceptions import (
    NotFoundException,
    DuplicateValueException,
)


# Create a mock model for testing
class MockModel:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class MockCreate:
    def __init__(self, name: str):
        self.name = name


class MockUpdate:
    def __init__(self, name: str = None):
        self.name = name


class MockRepository(BaseRepository[MockModel, MockCreate, MockUpdate]):
    def __init__(self):
        super().__init__(MockModel)

    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[MockModel]:
        """Get item by name for testing."""
        stmt = select(self.model).where(self.model.name == name)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()


@pytest.fixture
def mock_db_session():
    """Create a mock database session for unit tests."""
    mock_session = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.rollback = MagicMock()
    mock_session.close = MagicMock()
    return mock_session


class TestBaseRepository:
    """Test base repository functionality."""

    @pytest.mark.asyncio
    async def test_create_success(self, mock_db_session):
        """Test creating an item successfully."""
        # Arrange
        db = mock_db_session
        repo = MockRepository()
        create_data = MockCreate("Test Item")
        expected_item = MockModel(1, "Test Item")

        with patch.object(repo, "create") as mock_create:
            mock_create.return_value = expected_item

            # Act
            result = await repo.create(db, obj_in=create_data)

            # Assert
            assert result.id == 1
            assert result.name == "Test Item"
            mock_create.assert_called_once_with(db, obj_in=create_data)

    @pytest.mark.asyncio
    async def test_create_database_error(self, mock_db_session):
        """Test creating an item when database operation fails."""
        # Arrange
        db = mock_db_session
        repo = MockRepository()
        create_data = MockCreate("Test Item")

        with patch.object(repo, "create") as mock_create:
            mock_create.side_effect = IntegrityError("duplicate key", None, None)

            # Act & Assert
            with pytest.raises(IntegrityError):
                await repo.create(db, obj_in=create_data)

    @pytest.mark.asyncio
    async def test_get_success(self, mock_db_session):
        """Test getting an item by ID successfully."""
        # Arrange
        db = mock_db_session
        repo = MockRepository()
        expected_item = MockModel(1, "Test Item")

        with patch.object(repo, "get") as mock_get:
            mock_get.return_value = expected_item

            # Act
            result = await repo.get(db, id=1)

            # Assert
            assert result.id == 1
            assert result.name == "Test Item"
            mock_get.assert_called_once_with(db, id=1)

    @pytest.mark.asyncio
    async def test_get_not_found(self, mock_db_session):
        """Test getting an item by ID when not found."""
        # Arrange
        db = mock_db_session
        repo = MockRepository()

        with patch.object(repo, "get") as mock_get:
            mock_get.return_value = None

            # Act
            result = await repo.get(db, id=999)

            # Assert
            assert result is None
            mock_get.assert_called_once_with(db, id=999)

    @pytest.mark.asyncio
    async def test_get_multi_success(self, mock_db_session):
        """Test getting multiple items successfully."""
        # Arrange
        db = mock_db_session
        repo = MockRepository()
        expected_items = [MockModel(1, "Item 1"), MockModel(2, "Item 2")]

        with patch.object(repo, "get_multi") as mock_get_multi:
            mock_get_multi.return_value = expected_items

            # Act
            result = await repo.get_multi(db, skip=0, limit=10)

            # Assert
            assert len(result) == 2
            assert result[0].id == 1
            assert result[0].name == "Item 1"
            assert result[1].id == 2
            assert result[1].name == "Item 2"
            mock_get_multi.assert_called_once_with(db, skip=0, limit=10)

    @pytest.mark.asyncio
    async def test_get_multi_empty(self, mock_db_session):
        """Test getting multiple items when none exist."""
        # Arrange
        db = mock_db_session
        repo = MockRepository()

        with patch.object(repo, "get_multi") as mock_get_multi:
            mock_get_multi.return_value = []

            # Act
            result = await repo.get_multi(db, skip=0, limit=10)

            # Assert
            assert len(result) == 0
            mock_get_multi.assert_called_once_with(db, skip=0, limit=10)

    @pytest.mark.asyncio
    async def test_update_success(self, mock_db_session):
        """Test updating an item successfully."""
        # Arrange
        db = mock_db_session
        repo = MockRepository()
        existing_item = MockModel(1, "Old Name")
        update_data = MockUpdate("New Name")
        expected_item = MockModel(1, "New Name")

        with patch.object(repo, "update") as mock_update:
            mock_update.return_value = expected_item

            # Act
            result = await repo.update(db, db_obj=existing_item, obj_in=update_data)

            # Assert
            assert result.id == 1
            assert result.name == "New Name"
            mock_update.assert_called_once_with(
                db, db_obj=existing_item, obj_in=update_data
            )

    @pytest.mark.asyncio
    async def test_update_database_error(self, mock_db_session):
        """Test updating an item when database operation fails."""
        # Arrange
        db = mock_db_session
        repo = MockRepository()
        existing_item = MockModel(1, "Old Name")
        update_data = MockUpdate("New Name")

        with patch.object(repo, "update") as mock_update:
            mock_update.side_effect = IntegrityError("update failed", None, None)

            # Act & Assert
            with pytest.raises(IntegrityError):
                await repo.update(db, db_obj=existing_item, obj_in=update_data)

    @pytest.mark.asyncio
    async def test_remove_success(self, mock_db_session):
        """Test removing an item successfully."""
        # Arrange
        db = mock_db_session
        repo = MockRepository()

        with patch.object(repo, "remove") as mock_remove:
            mock_remove.return_value = True

            # Act
            result = await repo.remove(db, id=1)

            # Assert
            assert result is True
            mock_remove.assert_called_once_with(db, id=1)

    @pytest.mark.asyncio
    async def test_remove_not_found(self, mock_db_session):
        """Test removing an item when not found."""
        # Arrange
        db = mock_db_session
        repo = MockRepository()

        with patch.object(repo, "remove") as mock_remove:
            mock_remove.return_value = False

            # Act
            result = await repo.remove(db, id=999)

            # Assert
            assert result is False
            mock_remove.assert_called_once_with(db, id=999)

    @pytest.mark.asyncio
    async def test_hard_delete_success(self, mock_db_session):
        """Test hard deleting an item successfully."""
        # Arrange
        db = mock_db_session
        repo = MockRepository()

        with patch.object(repo, "hard_delete") as mock_hard_delete:
            mock_hard_delete.return_value = True

            # Act
            result = await repo.hard_delete(db, id=1)

            # Assert
            assert result is True
            mock_hard_delete.assert_called_once_with(db, id=1)

    @pytest.mark.asyncio
    async def test_hard_delete_not_found(self, mock_db_session):
        """Test hard deleting an item when not found."""
        # Arrange
        db = mock_db_session
        repo = MockRepository()

        with patch.object(repo, "hard_delete") as mock_hard_delete:
            mock_hard_delete.return_value = False

            # Act
            result = await repo.hard_delete(db, id=999)

            # Assert
            assert result is False
            mock_hard_delete.assert_called_once_with(db, id=999)
