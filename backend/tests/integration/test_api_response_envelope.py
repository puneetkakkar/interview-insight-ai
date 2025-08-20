import pytest
from fastapi.testclient import TestClient


class TestAPIResponseEnvelope:
    """Test consistent API response envelope structure."""

    def test_health_success_envelope(self, mock_client: TestClient):
        """Test health endpoint returns success envelope."""
        response = mock_client.get("/health")
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["data"], dict)
        assert body["data"]["status"] == "healthy"

    def test_root_success_envelope(self, mock_client: TestClient):
        """Test root endpoint returns success envelope."""
        response = mock_client.get("/")
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["data"], dict)
        assert "version" in body["data"]

    def test_info_success_envelope(self, mock_client: TestClient):
        """Test info endpoint returns success envelope."""
        response = mock_client.get("/info")
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["data"], dict)
        assert body["data"]["status"] == "running"

    def test_validation_error_envelope(self, mock_client: TestClient):
        """Test validation errors return consistent error envelope."""
        # limit must be >= 1; sending 0 triggers validation error
        response = mock_client.get("/api/v1/items", params={"limit": 0})
        assert response.status_code == 422
        body = response.json()
        assert body["success"] is False
        assert body["data"] is None
        assert "error" in body
        assert body["error"]["code"] == 422
        assert body["error"]["message"] == "Validation Error"
        assert isinstance(body["error"]["details"], list)
        assert any(
            d.get("type") == "greater_than_equal" or d.get("msg", "").lower().find("greater than or equal") != -1
            for d in body["error"]["details"]
        )

    def test_validation_error_missing_required_fields(self, mock_client: TestClient):
        """Test validation errors for missing required fields."""
        response = mock_client.post("/api/v1/items/", json={})
        assert response.status_code == 422
        body = response.json()
        assert body["success"] is False
        assert body["data"] is None
        assert body["error"]["code"] == 422
        assert body["error"]["message"] == "Validation Error"
        assert isinstance(body["error"]["details"], list)

    def test_validation_error_invalid_data_types(self, mock_client: TestClient):
        """Test validation errors for invalid data types."""
        response = mock_client.post("/api/v1/items/", json={"title": 123, "price": "invalid"})
        assert response.status_code == 422
        body = response.json()
        assert body["success"] is False
        assert body["data"] is None
        assert body["error"]["code"] == 422
        assert body["error"]["message"] == "Validation Error"

    def test_validation_error_pagination_limits(self, mock_client: TestClient):
        """Test validation errors for pagination parameter limits."""
        # Test negative skip
        response = mock_client.get("/api/v1/items", params={"skip": -1})
        assert response.status_code == 422
        body = response.json()
        assert body["success"] is False
        assert body["error"]["code"] == 422

        # Test limit too high
        response = mock_client.get("/api/v1/items", params={"limit": 1001})
        assert response.status_code == 422
        body = response.json()
        assert body["success"] is False
        assert body["error"]["code"] == 422

    def test_response_envelope_structure_consistency(self, mock_client: TestClient):
        """Test all success responses follow consistent envelope structure."""
        # Test health endpoint
        response = mock_client.get("/health")
        body = response.json()
        assert "success" in body
        assert "data" in body
        assert body["success"] is True
        assert body["data"] is not None

        # Test root endpoint
        response = mock_client.get("/")
        body = response.json()
        assert "success" in body
        assert "data" in body
        assert body["success"] is True
        assert body["data"] is not None

        # Test info endpoint
        response = mock_client.get("/info")
        body = response.json()
        assert "success" in body
        assert "data" in body
        assert body["success"] is True
        assert body["data"] is not None

    def test_error_envelope_structure_consistency(self, mock_client: TestClient):
        """Test all error responses follow consistent envelope structure."""
        # Test validation error
        response = mock_client.get("/api/v1/items", params={"limit": 0})
        body = response.json()
        assert "success" in body
        assert "data" in body
        assert "error" in body
        assert body["success"] is False
        assert body["data"] is None
        assert "code" in body["error"]
        assert "message" in body["error"]
        assert "details" in body["error"]
