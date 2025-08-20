from fastapi import FastAPI

from .core.setup import create_application
from .api.v1 import items
from .core.response import build_success_response

# Create the FastAPI application
app = create_application()

# Include API routers
app.include_router(items.router, prefix="/api/v1")

# Add root endpoint
@app.get("/")
async def root() -> dict[str, object]:
    """Root endpoint with basic information."""
    return build_success_response({
        "message": "FastAPI Minimal Boilerplate",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    })

# Add info endpoint
@app.get("/info")
async def info() -> dict[str, object]:
    """Application information endpoint."""
    return build_success_response({
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
            "Clean architecture"
        ]
    })

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
