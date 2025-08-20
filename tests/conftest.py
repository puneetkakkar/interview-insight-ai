import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.app.core.config import settings
from src.app.core.db.database import Base, get_db
from src.app.main import app


# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
)

# Create test session factory
TestingSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db_setup() -> AsyncGenerator[None, None]:
    """Setup test database."""
    async with test_engine.begin() as conn:
        # Import all models here to ensure they are registered
        from src.app.models import Item  # noqa: F401

        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(test_db_setup: None) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
def test_app() -> FastAPI:
    """Create a test app without database initialization."""
    from src.app.core.setup import (
        _configure_cors,
        _configure_exception_handlers,
        _configure_routes,
        _configure_access_logging,
    )
    from src.app.api.v1 import items
    from src.app.core.response import build_success_response

    # Create app without lifespan (database initialization)
    test_app = FastAPI(
        title="Test App",
        description="Test application without database",
        version="0.1.0",
        debug=True,
    )

    # Apply all configurations except lifespan
    _configure_cors(test_app)
    _configure_access_logging(test_app)
    _configure_exception_handlers(test_app)
    _configure_routes(test_app)

    # Include API routers
    test_app.include_router(items.router, prefix="/api/v1")

    # Add root endpoint
    @test_app.get("/")
    async def root() -> dict[str, object]:
        """Root endpoint with basic information."""
        return build_success_response(
            {
                "message": "FastAPI Minimal Boilerplate",
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
                "name": "FastAPI Minimal Boilerplate",
                "description": "A minimal, production-ready FastAPI boilerplate",
                "version": "0.1.0",
                "status": "running",
                "features": [
                    "FastAPI with async support",
                    "SQLAlchemy 2.0 + PostgreSQL",
                    "Pydantic V2 schemas",
                    "Alembic migrations",
                    "Docker Compose setup",
                    "Comprehensive testing",
                    "Type hints throughout",
                    "Clean architecture",
                ],
            }
        )

    return test_app


@pytest.fixture
def client(db_session: AsyncSession) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def mock_client(test_app: FastAPI) -> Generator[TestClient, None, None]:
    """Create a test client without database dependency override."""
    with TestClient(test_app) as test_client:
        yield test_client


@pytest_asyncio.fixture
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def mock_db_session() -> MagicMock:
    """Create a mock database session for unit tests."""
    mock_session = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.rollback = MagicMock()
    mock_session.close = MagicMock()
    return mock_session


@pytest.fixture
def sample_item_data() -> dict:
    """Sample item data for testing."""
    return {
        "title": "Test Item",
        "description": "A test item for testing purposes",
        "price": 29.99,
        "is_active": True,
    }


@pytest.fixture
def sample_item_update_data() -> dict:
    """Sample item update data for testing."""
    return {
        "title": "Updated Test Item",
        "description": "An updated test item",
        "price": 39.99,
        "is_active": False,
    }


@pytest.fixture
def pagination_params() -> dict:
    """Sample pagination parameters for testing."""
    return {"skip": 0, "limit": 10}


@pytest.fixture
def search_params() -> dict:
    """Sample search parameters for testing."""
    return {"title": "test", "skip": 0, "limit": 10}
