import pytest
from fastapi.testclient import TestClient

from tests.conftest import mock_client


class TestAPIResponseEnvelope:
    """Test API response envelope structure consistency."""

    def test_success_response_envelope_structure(self, mock_client: TestClient):
        """Test success responses follow consistent envelope structure."""
        # Test health endpoint
        response = mock_client.get("/health")
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "data" in body
        assert body["data"]["status"] == "healthy"
        assert body["data"]["service"] == "Interview Insight AI"

    def test_root_endpoint_response_structure(self, mock_client: TestClient):
        """Test that root endpoint returns expected response structure."""
        response = mock_client.get("/")
        assert response.status_code == 200
        
        body = response.json()
        assert "success" in body
        assert "message" in body
        assert "data" in body
        
        # Check data structure
        data = body["data"]
        assert "service" in data
        assert "version" in data
        assert "status" in data
        assert "timestamp" in data
        
        # Check specific values
        assert body["data"]["service"] == "InterviewInsight AI"
        assert body["data"]["status"] == "running"

    def test_info_endpoint_response_structure(self, mock_client: TestClient):
        """Test that info endpoint returns expected response structure."""
        response = mock_client.get("/info")
        assert response.status_code == 200
        
        body = response.json()
        assert "success" in body
        assert "message" in body
        assert "data" in body
        
        # Check data structure
        data = body["data"]
        assert "name" in data
        assert "description" in data
        assert "version" in data
        assert "environment" in data
        assert "storage_type" in data
        assert "features" in data
        assert "ai_models" in data
        assert "timestamp" in data
        
        # Check specific values
        assert "InterviewInsight" in body["data"]["message"]

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

    def test_method_not_allowed_envelope(self, mock_client: TestClient):
        """Test method not allowed responses follow error envelope structure."""
        # Test POST to GET-only endpoints
        response = mock_client.post("/")
        assert response.status_code == 405
        body = response.json()
        assert "success" in body
        assert "data" in body
        assert "error" in body
        assert body["success"] is False
        assert body["data"] is None
        assert "code" in body["error"]
        assert "message" in body["error"]
        assert body["error"]["code"] == 405

        response = mock_client.post("/info")
        assert response.status_code == 405
        body = response.json()
        assert body["success"] is False
        assert body["error"]["code"] == 405

        response = mock_client.post("/health")
        assert response.status_code == 405
        body = response.json()
        assert body["success"] is False
        assert body["error"]["code"] == 405

    def test_error_envelope_structure_consistency(self, mock_client: TestClient):
        """Test all error responses follow consistent envelope structure."""
        # Test method not allowed error
        response = mock_client.post("/")
        body = response.json()
        assert "success" in body
        assert "data" in body
        assert "error" in body
        assert body["success"] is False
        assert body["data"] is None
        assert "code" in body["error"]
        assert "message" in body["error"]

    def test_response_content_type_consistency(self, mock_client: TestClient):
        """Test all responses return consistent content type."""
        # Test success responses
        response = mock_client.get("/health")
        assert response.headers["content-type"] == "application/json"
        
        response = mock_client.get("/")
        assert response.headers["content-type"] == "application/json"
        
        response = mock_client.get("/info")
        assert response.headers["content-type"] == "application/json"

        # Test error responses
        response = mock_client.post("/")
        assert response.headers["content-type"] == "application/json"

    def test_response_data_types(self, mock_client: TestClient):
        """Test response data types are consistent."""
        # Test health endpoint data types
        response = mock_client.get("/health")
        body = response.json()
        assert isinstance(body["success"], bool)
        assert isinstance(body["data"], dict)
        assert isinstance(body["data"]["status"], str)
        assert isinstance(body["data"]["service"], str)

        # Test root endpoint data types
        response = mock_client.get("/")
        body = response.json()
        assert isinstance(body["success"], bool)
        assert isinstance(body["data"], dict)
        assert isinstance(body["data"]["message"], str)
        assert isinstance(body["data"]["version"], str)

        # Test info endpoint data types
        response = mock_client.get("/info")
        body = response.json()
        assert isinstance(body["success"], bool)
        assert isinstance(body["data"], dict)
        assert isinstance(body["data"]["name"], str)
        assert isinstance(body["data"]["version"], str)
        assert isinstance(body["data"]["status"], str)
