from contextlib import asynccontextmanager
from typing import AsyncGenerator
import time
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from langgraph.store.memory import InMemoryStore
from starlette.exceptions import HTTPException as StarletteHTTPException
from langgraph.checkpoint.memory import InMemorySaver

from src.app.agents.agent import get_all_agent_info, get_agent

from .config import settings
from .db.database import close_db, init_db
from .logger import logger
from .response import build_success_response
from .exceptions.handlers import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager: startup/shutdown hooks."""
    logger.info("Starting up FastAPI Application...")
    try:
        await init_db()
        logger.info("Database initialized successfully")
        # Configure agents with both memory components
        agents = get_all_agent_info()
        for a in agents:
            agent = get_agent(a.key)
            # Set checkpointer for thread-scoped memory (conversation history)
            agent.checkpointer = InMemorySaver()
            # Set store for long-term memory (cross-conversation knowledge)
            agent.store = InMemoryStore()
        logger.info("Agents memory components initialized successfully")
        yield
    except Exception as exc:
        logger.error(f"Failed to initialize database/agents: {exc}")
        raise

    logger.info("Shutting down FastAPI Application...")
    await close_db()
    logger.info("Database connections closed")
    logger.info("Agents memory components closed")


def _configure_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Tighten for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _configure_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)


def _configure_routes(app: FastAPI) -> None:
    @app.get("/health")
    async def health_check() -> dict[str, object]:
        return build_success_response(
            {"status": "healthy", "service": settings.APP_NAME}
        )


def _configure_access_logging(app: FastAPI) -> None:
    @app.middleware("http")
    async def access_log_middleware(request, call_next):  # type: ignore[override]
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        try:
            request.state.request_id = request_id
        except Exception:
            pass
        start_time = time.time()
        path = request.url.path
        method = request.method
        try:
            response = await call_next(request)
            status_code = response.status_code
            duration_ms = int((time.time() - start_time) * 1000)
            logger.info(
                "access",
                extra={
                    "request_id": request_id,
                    "path": path,
                    "method": method,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                },
            )
            response.headers["x-request-id"] = request_id
            return response
        except Exception:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.error(
                "access_error",
                extra={
                    "request_id": request_id,
                    "path": path,
                    "method": method,
                    "status_code": 500,
                    "duration_ms": duration_ms,
                },
            )
            raise


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    _configure_cors(app)
    _configure_access_logging(app)
    _configure_exception_handlers(app)
    _configure_routes(app)

    return app
