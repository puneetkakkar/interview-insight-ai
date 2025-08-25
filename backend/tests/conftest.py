import asyncio
import os
from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.app.core.setup import (
    _configure_cors,
    _configure_exception_handlers,
    _configure_routes,
    _configure_access_logging,
)
from src.app.core.response import build_success_response


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    # Ensure we're in testing environment
    os.environ["ENVIRONMENT"] = "testing"
    os.environ["DEBUG"] = "false"
    os.environ["RELOAD"] = "false"
    yield
    # Clean up
    if "ENVIRONMENT" in os.environ:
        del os.environ["ENVIRONMENT"]
    if "DEBUG" in os.environ:
        del os.environ["DEBUG"]
    if "RELOAD" in os.environ:
        del os.environ["RELOAD"]


@pytest.fixture
def test_app() -> FastAPI:
    """Create a test app without database initialization."""
    # Create app without lifespan (database initialization)
    test_app = FastAPI(
        title="Test App",
        description="Test application without database",
        version="0.1.0",
        debug=False,  # Disable debug in testing
    )

    # Apply all configurations except lifespan
    _configure_cors(test_app)
    _configure_access_logging(test_app)
    _configure_exception_handlers(test_app)
    _configure_routes(test_app)

    # Include API routers
    # Note: Items router removed - only agent router available

    # Add root endpoint
    @test_app.get("/")
    async def root() -> dict[str, object]:
        """Root endpoint with basic information."""
        return build_success_response(
            {
                "message": "Interview Insight AI",
                "version": "0.1.0",
                "docs": "/docs",
                "health": "/health",
            }
        )

    # Add info endpoint
    @test_app.get("/info")
    async def info() -> dict[str, object]:
        """Application information endpoint."""
        return build_success_response(
            {
                "name": "Interview Insight AI",
                "description": "A production-ready Interview Insight AI",
                "version": "0.1.0",
                "status": "running",
            }
        )

    return test_app


@pytest.fixture
def mock_client(test_app: FastAPI) -> Generator[TestClient, None, None]:
    """Create a test client without database dependency override."""
    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture
def mock_db_session() -> MagicMock:
    """Create a mock database session for unit tests."""
    mock_session = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.rollback = MagicMock()
    mock_session.close = MagicMock()
    return mock_session


@pytest.fixture
def sample_root_response():
    """Sample response for root endpoint."""
    return {
        "success": True,
        "message": "InterviewInsight AI",
        "data": {
            "service": "InterviewInsight AI",
            "version": "1.0.0",
            "status": "running",
            "timestamp": "2024-01-01T00:00:00",
        },
    }

@pytest.fixture
def sample_info_response():
    """Sample response for info endpoint."""
    return {
        "success": True,
        "message": "Application information retrieved successfully",
        "data": {
            "name": "InterviewInsight AI",
            "description": "A production-ready AI-powered interview transcript analysis platform",
            "version": "1.0.0",
            "environment": "development",
            "storage_type": "memory",
            "features": [
                "Multi-Agent AI System",
                "Interview Transcript Analysis",
                "Entity Recognition",
                "Sentiment Analysis",
                "Timeline Extraction",
                "Research Assistant",
                "Web Search Integration",
                "Mathematical Calculations",
            ],
            "ai_models": ["fake-model"],
            "timestamp": "2024-01-01T00:00:00",
        },
    }


# Item-related fixtures removed - no longer needed
