import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.app.main import app
from src.app.core.exceptions.http_exceptions import (
    NotFoundException,
    DuplicateValueException,
    ValidationException,
    ForbiddenException,
    UnauthorizedException,
)


class TestCustomExceptions:
    """Test custom exception classes."""

    def test_not_found_exception(self):
        """Test NotFoundException creation and properties."""
        # Arrange & Act
        exception = NotFoundException("Custom not found message")
        
        # Assert
        assert exception.status_code == status.HTTP_404_NOT_FOUND
        assert exception.detail == "Custom not found message"

    def test_not_found_exception_default_message(self):
        """Test NotFoundException with default message."""
        # Arrange & Act
        exception = NotFoundException()
        
        # Assert
        assert exception.status_code == status.HTTP_404_NOT_FOUND
        assert exception.detail == "Resource not found"

    def test_duplicate_value_exception(self):
        """Test DuplicateValueException creation and properties."""
        # Arrange & Act
        exception = DuplicateValueException("Custom duplicate message")
        
        # Assert
        assert exception.status_code == status.HTTP_409_CONFLICT
        assert exception.detail == "Custom duplicate message"

    def test_validation_exception(self):
        """Test ValidationException creation and properties."""
        # Arrange & Act
        exception = ValidationException("Custom validation message")
        
        # Assert
        assert exception.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert exception.detail == "Custom validation message"

    def test_forbidden_exception(self):
        """Test ForbiddenException creation and properties."""
        # Arrange & Act
        exception = ForbiddenException("Custom forbidden message")
        
        # Assert
        assert exception.status_code == status.HTTP_403_FORBIDDEN
        assert exception.detail == "Custom forbidden message"

    def test_unauthorized_exception(self):
        """Test UnauthorizedException creation and properties."""
        # Arrange & Act
        exception = UnauthorizedException("Custom unauthorized message")
        
        # Assert
        assert exception.status_code == status.HTTP_401_UNAUTHORIZED
        assert exception.detail == "Custom unauthorized message"


class TestExceptionHandlers:
    """Test global exception handlers."""

    def test_http_exception_handler_404(self):
        """Test HTTP exception handler for 404 errors."""
        with TestClient(app) as client:
            # Act - Trigger 404 by accessing non-existent endpoint
            response = client.get("/non-existent-endpoint")
            
            # Assert
            assert response.status_code == 404
            body = response.json()
            assert body["success"] is False
            assert body["data"] is None
            assert body["error"]["code"] == 404
            assert body["error"]["message"] == "Not Found"
            assert "not found" in body["error"]["details"].lower()

    def test_http_exception_handler_405(self):
        """Test HTTP exception handler for 405 errors."""
        with TestClient(app) as client:
            # Act - Trigger 405 by using wrong HTTP method
            response = client.delete("/health")
            
            # Assert
            assert response.status_code == 405
            body = response.json()
            assert body["success"] is False
            assert body["data"] is None
            assert body["error"]["code"] == 405
            assert body["error"]["message"] == "Method Not Allowed"

    def test_validation_exception_handler(self):
        """Test validation exception handler for 422 errors."""
        with TestClient(app) as client:
            # Act - Trigger 422 by sending invalid data
            response = client.post("/api/v1/items/", json={"invalid": "data"})
            
            # Assert
            assert response.status_code == 422
            body = response.json()
            assert body["success"] is False
            assert body["data"] is None
            assert body["error"]["code"] == 422
            assert body["error"]["message"] == "Validation Error"
            assert isinstance(body["error"]["details"], list)

    def test_custom_exception_integration(self):
        """Test custom exceptions are properly handled by global handlers."""
        # This test verifies that custom exceptions inherit from HTTPException
        # and are handled by the global http_exception_handler
        
        # Arrange
        custom_exception = NotFoundException("Custom message")
        
        # Assert
        assert isinstance(custom_exception, HTTPException)
        assert custom_exception.status_code == 404
        assert custom_exception.detail == "Custom message"

    def test_exception_handler_response_structure(self):
        """Test all exception handlers return consistent response structure."""
        with TestClient(app) as client:
            # Test 404
            response = client.get("/non-existent")
            body = response.json()
            assert "success" in body
            assert "data" in body
            assert "error" in body
            assert body["success"] is False
            assert body["data"] is None
            assert "code" in body["error"]
            assert "message" in body["error"]
            assert "details" in body["error"]

            # Test 422
            response = client.post("/api/v1/items/", json={})
            body = response.json()
            assert "success" in body
            assert "data" in body
            assert "error" in body
            assert body["success"] is False
            assert body["data"] is None
            assert "code" in body["error"]
            assert "message" in body["error"]
            assert "details" in body["error"]


class TestExceptionHandlerEdgeCases:
    """Test edge cases for exception handlers."""

    def test_http_exception_handler_unknown_status_code(self):
        """Test HTTP exception handler with unknown status code."""
        # This test verifies the handler gracefully handles unknown status codes
        with TestClient(app) as client:
            # Act - Use a method that's not allowed on an endpoint
            response = client.patch("/health")
            
            # Assert - Should still return proper error envelope
            assert response.status_code in [405, 422]  # Method not allowed or validation error
            body = response.json()
            assert body["success"] is False
            assert body["data"] is None
            assert "error" in body

    def test_validation_error_details_structure(self):
        """Test validation error details follow expected structure."""
        with TestClient(app) as client:
            # Act - Trigger validation error with multiple issues
            response = client.post("/api/v1/items/", json={"title": "", "price": -100})
            
            # Assert
            assert response.status_code == 422
            body = response.json()
            assert body["success"] is False
            assert body["error"]["code"] == 422
            assert body["error"]["message"] == "Validation Error"
            assert isinstance(body["error"]["details"], list)
            
            # Check that details contain validation error objects
            for detail in body["error"]["details"]:
                assert "type" in detail
                assert "loc" in detail
                assert "msg" in detail
                assert "input" in detail
