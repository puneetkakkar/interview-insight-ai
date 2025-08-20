import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from src.app.main import app


class TestMainEndpoints:
    """Test main application endpoints."""

    def test_root_endpoint(self):
        """Test root endpoint returns correct response structure."""
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.get("/")
        
        # Assert
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "data" in body
        assert "message" in body["data"]
        assert "FRAI" in body["data"]["message"]

    def test_info_endpoint(self):
        """Test info endpoint returns correct response structure."""
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.get("/info")
        
        # Assert
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "data" in body
        assert "name" in body["data"]
        assert "version" in body["data"]
        assert "description" in body["data"]

    def test_root_endpoint_response_structure(self):
        """Test root endpoint response structure in detail."""
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.get("/")
        
        # Assert
        assert response.status_code == 200
        body = response.json()
        assert "success" in body
        assert "data" in body
        assert "message" not in body  # message is inside data
        assert body["success"] is True
        assert isinstance(body["data"], dict)
        assert "message" in body["data"]
        assert "version" in body["data"]
        assert "docs" in body["data"]
        assert "health" in body["data"]

    def test_info_endpoint_response_structure(self):
        """Test info endpoint response structure in detail."""
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.get("/info")
        
        # Assert
        assert response.status_code == 200
        body = response.json()
        assert "success" in body
        assert "data" in body
        assert body["success"] is True
        assert isinstance(body["data"], dict)
        assert "name" in body["data"]
        assert "version" in body["data"]
        assert "description" in body["data"]
        assert "status" in body["data"]

    def test_root_endpoint_content_type(self):
        """Test root endpoint returns correct content type."""
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.get("/")
        
        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_info_endpoint_content_type(self):
        """Test info endpoint returns correct content type."""
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.get("/info")
        
        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_root_endpoint_method_not_allowed(self):
        """Test root endpoint with wrong HTTP method."""
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.post("/")
        
        # Assert
        assert response.status_code == 405
        body = response.json()
        assert body["success"] is False
        assert "error" in body
        assert body["error"]["code"] == 405

    def test_info_endpoint_method_not_allowed(self):
        """Test info endpoint with wrong HTTP method."""
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.post("/info")
        
        # Assert
        assert response.status_code == 405
        body = response.json()
        assert body["success"] is False
        assert "error" in body
        assert body["error"]["code"] == 405

    def test_root_endpoint_data_values(self):
        """Test root endpoint returns expected data values."""
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.get("/")
        
        # Assert
        assert response.status_code == 200
        body = response.json()
        data = body["data"]
        assert data["message"] == "FRAI Boilerplate"
        assert data["version"] == "0.1.0"
        assert data["docs"] == "/docs"
        assert data["health"] == "/health"

    def test_info_endpoint_data_values(self):
        """Test info endpoint returns expected data values."""
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.get("/info")
        
        # Assert
        assert response.status_code == 200
        body = response.json()
        data = body["data"]
        assert data["name"] == "FRAI Boilerplate"
        assert data["version"] == "0.1.0"
        assert data["description"] == "A production-ready FRAI boilerplate"
        assert data["status"] == "running"

    def test_root_endpoint_no_optional_fields(self):
        """Test root endpoint doesn't have unexpected fields."""
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.get("/")
        
        # Assert
        assert response.status_code == 200
        body = response.json()
        # Should only have success, data, and data.message, data.version, data.docs, data.health
        expected_keys = {"success", "data"}
        assert set(body.keys()) == expected_keys
        expected_data_keys = {"message", "version", "docs", "health"}
        assert set(body["data"].keys()) == expected_data_keys

    def test_info_endpoint_no_optional_fields(self):
        """Test info endpoint doesn't have unexpected fields."""
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.get("/info")
        
        # Assert
        assert response.status_code == 200
        body = response.json()
        # Should only have success, data, and data.name, data.version, data.description, data.status
        expected_keys = {"success", "data"}
        assert set(body.keys()) == expected_keys
        expected_data_keys = {"name", "version", "description", "status"}
        assert set(body["data"].keys()) == expected_data_keys
