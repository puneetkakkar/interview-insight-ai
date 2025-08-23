import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.datastructures import State
from starlette.requests import Request as StarletteRequest
from starlette.responses import Response
from pydantic import ValidationError

from src.app.core.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler
)
from src.app.core.exceptions.http_exceptions import (
    NotFoundException,
    DuplicateValueException,
    ValidationException,
    ForbiddenException,
    UnauthorizedException
)
from src.app.core.response import build_error_response


class TestCustomExceptions:
    """Test custom HTTP exceptions."""

    def test_not_found_exception(self):
        """Test NotFoundException instantiation and properties."""
        # Arrange & Act
        exc = NotFoundException("Resource not found")
        
        # Assert
        assert exc.status_code == 404
        assert exc.detail == "Resource not found"
        assert isinstance(exc, HTTPException)

    def test_not_found_exception_default_message(self):
        """Test NotFoundException with default message."""
        # Arrange & Act
        exc = NotFoundException()
        
        # Assert
        assert exc.status_code == 404
        assert exc.detail == "Resource not found"
        assert isinstance(exc, HTTPException)

    def test_duplicate_value_exception(self):
        """Test DuplicateValueException instantiation and properties."""
        # Arrange & Act
        exc = DuplicateValueException("Title already exists")
        
        # Assert
        assert exc.status_code == 409
        assert exc.detail == "Title already exists"
        assert isinstance(exc, HTTPException)

    def test_validation_exception(self):
        """Test ValidationException instantiation and properties."""
        # Arrange & Act
        exc = ValidationException("Invalid input data")
        
        # Assert
        assert exc.status_code == 422
        assert exc.detail == "Invalid input data"
        assert isinstance(exc, HTTPException)

    def test_forbidden_exception(self):
        """Test ForbiddenException instantiation and properties."""
        # Arrange & Act
        exc = ForbiddenException("Access denied")
        
        # Assert
        assert exc.status_code == 403
        assert exc.detail == "Access denied"
        assert isinstance(exc, HTTPException)

    def test_unauthorized_exception(self):
        """Test UnauthorizedException instantiation and properties."""
        # Arrange & Act
        exc = UnauthorizedException("Authentication required")
        
        # Assert
        assert exc.status_code == 401
        assert exc.detail == "Authentication required"
        assert isinstance(exc, HTTPException)

    def test_exception_inheritance(self):
        """Test that custom exceptions properly inherit from HTTPException."""
        # Arrange & Act
        exceptions = [
            NotFoundException(),
            DuplicateValueException("test"),
            ValidationException("test"),
            ForbiddenException("test"),
            UnauthorizedException("test")
        ]
        
        # Assert
        for exc in exceptions:
            assert isinstance(exc, HTTPException)
            assert hasattr(exc, 'status_code')
            assert hasattr(exc, 'detail')


class TestExceptionHandlers:
    """Test global exception handlers."""

    @pytest.mark.asyncio
    async def test_http_exception_handler_404(self):
        """Test HTTP exception handler for 404 errors."""
        # Arrange
        exc = NotFoundException("Resource not found")
        request = MagicMock(spec=Request)
        
        # Act
        response = await http_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 404
        body = response.body.decode()
        assert "success" in body
        assert "false" in body
        assert "Resource not found" in body

    @pytest.mark.asyncio
    async def test_http_exception_handler_405(self):
        """Test HTTP exception handler for 405 errors."""
        # Arrange
        exc = HTTPException(status_code=405, detail="Method not allowed")
        request = MagicMock(spec=Request)
        
        # Act
        response = await http_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 405
        body = response.body.decode()
        assert "success" in body
        assert "false" in body
        assert "Method Not Allowed" in body

    @pytest.mark.asyncio
    async def test_http_exception_handler_custom_status(self):
        """Test HTTP exception handler for custom status codes."""
        # Arrange
        exc = HTTPException(status_code=418, detail="I'm a teapot")
        request = MagicMock(spec=Request)
        
        # Act
        response = await http_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 418
        body = response.body.decode()
        assert "success" in body
        assert "false" in body

    @pytest.mark.asyncio
    async def test_validation_exception_handler(self):
        """Test validation exception handler."""
        # Arrange
        errors = [
            {
                "type": "missing",
                "loc": ["body", "title"],
                "msg": "Field required",
                "input": None
            }
        ]
        exc = RequestValidationError(errors=errors)
        request = MagicMock(spec=Request)
        
        # Act
        response = await validation_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 422
        body = response.body.decode()
        assert "success" in body
        assert "false" in body
        assert "Validation Error" in body
        assert "Field required" in body

    @pytest.mark.asyncio
    async def test_validation_exception_handler_multiple_errors(self):
        """Test validation exception handler with multiple errors."""
        # Arrange
        errors = [
            {
                "type": "missing",
                "loc": ["body", "title"],
                "msg": "Field required",
                "input": None
            },
            {
                "type": "value_error",
                "loc": ["body", "price"],
                "msg": "Value error, got -10",
                "input": -10
            }
        ]
        exc = RequestValidationError(errors=errors)
        request = MagicMock(spec=Request)
        
        # Act
        response = await validation_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 422
        body = response.body.decode()
        assert "success" in body
        assert "false" in body
        assert "Validation Error" in body
        assert "Field required" in body
        assert "Value error" in body

    @pytest.mark.asyncio
    async def test_unhandled_exception_handler(self):
        """Test unhandled exception handler."""
        # Arrange
        exc = Exception("Unexpected error")
        request = MagicMock(spec=Request)
        
        # Act
        response = await unhandled_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 500
        body = response.body.decode()
        assert "success" in body
        assert "false" in body
        assert "Internal Server Error" in body

    @pytest.mark.asyncio
    async def test_unhandled_exception_handler_with_message(self):
        """Test unhandled exception handler with custom message."""
        # Arrange
        exc = ValueError("Invalid value")
        request = MagicMock(spec=Request)
        
        # Act
        response = await unhandled_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 500
        body = response.body.decode()
        assert "success" in body
        assert "false" in body
        assert "Internal Server Error" in body

    @pytest.mark.asyncio
    async def test_custom_exception_integration(self):
        """Test that custom exceptions are handled by global handlers."""
        # Arrange
        exc = DuplicateValueException("Title already exists")
        request = MagicMock(spec=Request)
        
        # Act
        response = await http_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 409
        body = response.body.decode()
        assert "success" in body
        assert "false" in body
        assert "Title already exists" in body

    @pytest.mark.asyncio
    async def test_exception_handler_response_structure(self):
        """Test that exception handlers return proper response structure."""
        # Arrange
        exc = NotFoundException("Resource not found")
        request = MagicMock(spec=Request)
        
        # Act
        response = await http_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 404
        body = response.body.decode()
        # Check JSON structure
        import json
        data = json.loads(body)
        assert "success" in data
        assert "data" in data
        assert "error" in data
        assert data["success"] is False
        assert data["data"] is None
        assert "code" in data["error"]
        assert "message" in data["error"]
        assert "details" in data["error"]


class TestExceptionHandlerEdgeCases:
    """Test edge cases for exception handlers."""

    @pytest.mark.asyncio
    async def test_http_exception_handler_unknown_status_code(self):
        """Test HTTP exception handler with unknown status code."""
        # Arrange
        exc = HTTPException(status_code=599, detail="Unknown error")
        request = MagicMock(spec=Request)
        
        # Act
        response = await http_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 599
        body = response.body.decode()
        assert "success" in body
        assert "false" in body

    @pytest.mark.asyncio
    async def test_validation_error_details_structure(self):
        """Test validation error details structure."""
        # Arrange
        errors = [
            {
                "type": "missing",
                "loc": ["body", "title"],
                "msg": "Field required",
                "input": None
            }
        ]
        exc = RequestValidationError(errors=errors)
        request = MagicMock(spec=Request)
        
        # Act
        response = await validation_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 422
        body = response.body.decode()
        import json
        data = json.loads(body)
        assert "error" in data
        assert "details" in data["error"]
        assert isinstance(data["error"]["details"], list)
        assert len(data["error"]["details"]) == 1
        detail = data["error"]["details"][0]
        assert "type" in detail
        assert "loc" in detail
        assert "msg" in detail
        assert "input" in detail

    @pytest.mark.asyncio
    async def test_validation_error_empty_errors(self):
        """Test validation exception handler with empty errors."""
        # Arrange
        exc = RequestValidationError(errors=[])
        request = MagicMock(spec=Request)
        
        # Act
        response = await validation_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 422
        body = response.body.decode()
        assert "success" in body
        assert "false" in body

    @pytest.mark.asyncio
    async def test_unhandled_exception_handler_none_exception(self):
        """Test unhandled exception handler with None exception."""
        # Arrange
        exc = None
        request = MagicMock(spec=Request)
        
        # Act
        response = await unhandled_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 500
        body = response.body.decode()
        assert "success" in body
        assert "false" in body
        assert "Internal Server Error" in body

    @pytest.mark.asyncio
    async def test_http_exception_handler_starlette_exception(self):
        """Test HTTP exception handler with Starlette HTTPException."""
        # Arrange
        exc = StarletteHTTPException(status_code=400, detail="Bad Request")
        request = MagicMock(spec=Request)
        
        # Act
        response = await http_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 400
        body = response.body.decode()
        assert "success" in body
        assert "false" in body

    @pytest.mark.asyncio
    async def test_exception_handler_content_type(self):
        """Test that exception handlers return proper content type."""
        # Arrange
        exc = NotFoundException("Resource not found")
        request = MagicMock(spec=Request)
        
        # Act
        response = await http_exception_handler(request, exc)
        
        # Assert
        assert response.headers["content-type"] == "application/json"

    @pytest.mark.asyncio
    async def test_validation_exception_handler_complex_errors(self):
        """Test validation exception handler with complex error structures."""
        # Arrange
        errors = [
            {
                "type": "missing",
                "loc": ["body", "nested", "field"],
                "msg": "Field required",
                "input": None
            },
            {
                "type": "type_error",
                "loc": ["body", "items", 0, "id"],
                "msg": "Input should be a valid integer",
                "input": "not_an_int"
            }
        ]
        exc = RequestValidationError(errors=errors)
        request = MagicMock(spec=Request)
        
        # Act
        response = await validation_exception_handler(request, exc)
        
        # Assert
        assert response.status_code == 422
        body = response.body.decode()
        import json
        data = json.loads(body)
        assert "error" in data
        assert "details" in data["error"]
        assert len(data["error"]["details"]) == 2
        # Check nested location
        assert data["error"]["details"][0]["loc"] == ["body", "nested", "field"]
        # Check array location
        assert data["error"]["details"][1]["loc"] == ["body", "items", 0, "id"]
