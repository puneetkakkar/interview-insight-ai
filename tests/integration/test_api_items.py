import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.item import Item
from src.app.schemas.item import ItemCreate, ItemUpdate
from tests.helpers.generators import generate_item_data
from tests.helpers.mocks import mock_item_data


class TestItemsAPI:
    """Test items API endpoints integration."""

    def test_create_item_success(self, mock_client: TestClient):
        """Test creating an item successfully via API."""
        # Arrange
        item_data = generate_item_data()
        expected_item = Item(**item_data)
        expected_item.id = 1
        
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.get_by_title = AsyncMock(return_value=None)
            mock_repo.create = AsyncMock(return_value=expected_item)
            
            # Act
            response = mock_client.post("/api/v1/items/", json=item_data)
            
            # Assert
            assert response.status_code == 201
            body = response.json()
            assert body["success"] is True
            assert body["data"]["id"] == 1
            assert body["data"]["title"] == item_data["title"]
            assert body["message"] == "Item created successfully"
            mock_repo.get_by_title.assert_called_once()
            mock_repo.create.assert_called_once()

    def test_create_item_duplicate_title_error(self, mock_client: TestClient):
        """Test creating an item with duplicate title returns error."""
        # Arrange
        item_data = generate_item_data()
        existing_item = Item(**item_data)
        existing_item.id = 1
        
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.get_by_title = AsyncMock(return_value=existing_item)
            
            # Act
            response = mock_client.post("/api/v1/items/", json=item_data)
            
            # Assert
            assert response.status_code == 409
            body = response.json()
            assert body["success"] is False
            assert body["data"] is None
            assert body["error"]["code"] == 409
            assert "already exists" in body["error"]["details"]

    def test_create_item_validation_error(self, mock_client: TestClient):
        """Test creating an item with invalid data returns validation error."""
        # Arrange
        invalid_data = {"title": "", "price": -10.0}  # Invalid: empty title, negative price
        
        # Act
        response = mock_client.post("/api/v1/items/", json=invalid_data)
        
        # Assert
        assert response.status_code == 422
        body = response.json()
        assert body["success"] is False
        assert body["data"] is None
        assert body["error"]["code"] == 422
        assert body["error"]["message"] == "Validation Error"
        assert isinstance(body["error"]["details"], list)

    def test_get_items_success(self, mock_client: TestClient):
        """Test getting items successfully via API."""
        # Arrange
        items_data = [mock_item_data(), mock_item_data()]
        expected_items = []
        for data in items_data:
            itm = Item(**{k: v for k, v in data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
            itm.id = data["id"]
            expected_items.append(itm)
        
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.get_active_items = AsyncMock(return_value=expected_items)
            
            # Act
            response = mock_client.get("/api/v1/items/")
            
            # Assert
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert len(body["data"]) == 2
            assert body["data"][0]["title"] == "Test Item"
            mock_repo.get_active_items.assert_called_once()

    def test_get_items_with_pagination(self, mock_client: TestClient):
        """Test getting items with pagination parameters."""
        # Arrange
        items_data = [mock_item_data()]
        expected_items = []
        for data in items_data:
            itm = Item(**{k: v for k, v in data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
            itm.id = data["id"]
            expected_items.append(itm)
        
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.get_active_items = AsyncMock(return_value=expected_items)
            
            # Act
            response = mock_client.get("/api/v1/items/?skip=10&limit=5")
            
            # Assert
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            mock_repo.get_active_items.assert_called_once_with(
                mock_repo.get_active_items.call_args[0][0], skip=10, limit=5
            )

    def test_get_items_with_search(self, mock_client: TestClient):
        """Test getting items with search parameter."""
        # Arrange
        items_data = [mock_item_data()]
        expected_items = []
        for data in items_data:
            itm = Item(**{k: v for k, v in data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
            itm.id = data["id"]
            expected_items.append(itm)
        
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.search_by_title = AsyncMock(return_value=expected_items)
            
            # Act
            response = mock_client.get("/api/v1/items/?search=test")
            
            # Assert
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            mock_repo.search_by_title.assert_called_once()

    def test_get_item_by_id_success(self, mock_client: TestClient):
        """Test getting a specific item by ID successfully."""
        # Arrange
        item_data = mock_item_data()
        expected_item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
        expected_item.id = item_data["id"]
        
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.get = AsyncMock(return_value=expected_item)
            
            # Act
            response = mock_client.get("/api/v1/items/1")
            
            # Assert
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert body["data"]["id"] == 1
            assert body["data"]["title"] == "Test Item"
            mock_repo.get.assert_called_once()

    def test_get_item_by_id_not_found(self, mock_client: TestClient):
        """Test getting an item by ID when not found returns 404."""
        # Arrange
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.get = AsyncMock(return_value=None)
            
            # Act
            response = mock_client.get("/api/v1/items/999")
            
            # Assert
            assert response.status_code == 404
            body = response.json()
            assert body["success"] is False
            assert body["data"] is None
            assert body["error"]["code"] == 404
            assert "not found" in body["error"]["details"]

    def test_get_item_by_id_deleted(self, mock_client: TestClient):
        """Test getting a deleted item returns 404."""
        # Arrange
        item_data = mock_item_data()
        item_data["is_deleted"] = True
        deleted_item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
        deleted_item.id = item_data["id"]
        deleted_item.is_deleted = True
        
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.get = AsyncMock(return_value=deleted_item)
            
            # Act
            response = mock_client.get("/api/v1/items/1")
            
            # Assert
            assert response.status_code == 404
            body = response.json()
            assert body["success"] is False
            assert "not found" in body["error"]["details"]

    def test_update_item_success(self, mock_client: TestClient):
        """Test updating an item successfully via API."""
        # Arrange
        item_data = mock_item_data()
        existing_item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
        existing_item.id = item_data["id"]
        update_data = {"title": "Updated Title", "price": 149.99}
        updated_item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"} | set(update_data.keys())}, **update_data)
        updated_item.id = item_data["id"]
        
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.get = AsyncMock(return_value=existing_item)
            mock_repo.get_by_title = AsyncMock(return_value=None)
            mock_repo.update = AsyncMock(return_value=updated_item)
            
            # Act
            response = mock_client.put("/api/v1/items/1", json=update_data)
            
            # Assert
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert body["data"]["title"] == "Updated Title"
            assert body["data"]["price"] == 149.99
            assert body["message"] == "Item updated successfully"

    def test_update_item_not_found(self, mock_client: TestClient):
        """Test updating a non-existent item returns 404."""
        # Arrange
        update_data = {"title": "Updated Title"}
        
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.get = AsyncMock(return_value=None)
            
            # Act
            response = mock_client.put("/api/v1/items/999", json=update_data)
            
            # Assert
            assert response.status_code == 404
            body = response.json()
            assert body["success"] is False
            assert "not found" in body["error"]["details"]

    def test_update_item_duplicate_title_error(self, mock_client: TestClient):
        """Test updating item with duplicate title returns error."""
        # Arrange
        item_data = mock_item_data()
        existing_item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
        existing_item.id = item_data["id"]
        update_data = {"title": "Conflicting Title"}
        conflicting_item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
        conflicting_item.id = 2
        conflicting_item.title = "Conflicting Title"
        
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.get = AsyncMock(return_value=existing_item)
            mock_repo.get_by_title = AsyncMock(return_value=conflicting_item)
            
            # Act
            response = mock_client.put("/api/v1/items/1", json=update_data)
            
            # Assert
            assert response.status_code == 409
            body = response.json()
            assert body["success"] is False
            assert "already exists" in body["error"]["details"]

    def test_delete_item_success(self, mock_client: TestClient):
        """Test deleting an item successfully via API."""
        # Arrange
        item_data = mock_item_data()
        existing_item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
        existing_item.id = item_data["id"]
        
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.get = AsyncMock(return_value=existing_item)
            mock_repo.remove = AsyncMock(return_value=existing_item)
            
            # Act
            response = mock_client.delete("/api/v1/items/1")
            
            # Assert
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert body["data"]["id"] == 1
            assert body["message"] == "Item deleted successfully"
            mock_repo.remove.assert_called_once()

    def test_delete_item_not_found(self, mock_client: TestClient):
        """Test deleting a non-existent item returns 404."""
        # Arrange
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.get = AsyncMock(return_value=None)
            
            # Act
            response = mock_client.delete("/api/v1/items/999")
            
            # Assert
            assert response.status_code == 404
            body = response.json()
            assert body["success"] is False
            assert "not found" in body["error"]["details"]

    def test_search_items_success(self, mock_client: TestClient):
        """Test searching items by title successfully."""
        # Arrange
        items_data = [mock_item_data()]
        expected_items = []
        for data in items_data:
            itm = Item(**{k: v for k, v in data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
            itm.id = data["id"]
            expected_items.append(itm)
        
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.search_by_title = AsyncMock(return_value=expected_items)
            
            # Act
            response = mock_client.get("/api/v1/items/search/test")
            
            # Assert
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert len(body["data"]) == 1
            mock_repo.search_by_title.assert_called_once()

    def test_search_items_empty_results(self, mock_client: TestClient):
        """Test searching items with no results returns empty array."""
        # Arrange
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.search_by_title = AsyncMock(return_value=[])
            
            # Act
            response = mock_client.get("/api/v1/items/search/nonexistent")
            
            # Assert
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert body["data"] == []

    def test_search_items_with_pagination(self, mock_client: TestClient):
        """Test searching items with pagination parameters."""
        # Arrange
        items_data = [mock_item_data()]
        expected_items = []
        for data in items_data:
            itm = Item(**{k: v for k, v in data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
            itm.id = data["id"]
            expected_items.append(itm)
        
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.search_by_title = AsyncMock(return_value=expected_items)
            
            # Act
            response = mock_client.get("/api/v1/items/search/test?skip=5&limit=10")
            
            # Assert
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            mock_repo.search_by_title.assert_called_once()


class TestItemsAPIEdgeCases:
    """Test edge cases and error scenarios for items API."""

    def test_get_items_invalid_pagination_parameters(self, mock_client: TestClient):
        """Test getting items with invalid pagination parameters."""
        # Arrange
        # Act - Test negative skip
        response = mock_client.get("/api/v1/items/?skip=-1")
        
        # Assert
        assert response.status_code == 422
        body = response.json()
        assert body["success"] is False
        assert body["error"]["code"] == 422

    def test_get_items_limit_too_high(self, mock_client: TestClient):
        """Test getting items with limit exceeding maximum."""
        # Arrange
        # Act - Test limit > 1000
        response = mock_client.get("/api/v1/items/?limit=1001")
        
        # Assert
        assert response.status_code == 422
        body = response.json()
        assert body["success"] is False
        assert body["error"]["code"] == 422

    def test_create_item_missing_required_fields(self, mock_client: TestClient):
        """Test creating item with missing required fields."""
        # Arrange
        incomplete_data = {"description": "Only description provided"}
        
        # Act
        response = mock_client.post("/api/v1/items/", json=incomplete_data)
        
        # Assert
        assert response.status_code == 422
        body = response.json()
        assert body["success"] is False
        assert body["error"]["code"] == 422

    def test_update_item_no_changes(self, mock_client: TestClient):
        """Test updating item with no actual changes."""
        # Arrange
        item_data = mock_item_data()
        existing_item = Item(**{k: v for k, v in item_data.items() if k not in {"id", "created_at", "updated_at", "is_deleted", "deleted_at"}})
        existing_item.id = item_data["id"]
        update_data = {"title": existing_item.title, "price": existing_item.price}
        
        with patch("src.app.api.v1.items.items_repository") as mock_repo:
            mock_repo.get = AsyncMock(return_value=existing_item)
            mock_repo.get_by_title = AsyncMock(return_value=None)
            mock_repo.update = AsyncMock(return_value=existing_item)
            
            # Act
            response = mock_client.put("/api/v1/items/1", json=update_data)
            
            # Assert
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert body["data"]["title"] == existing_item.title
            assert body["data"]["price"] == existing_item.price
