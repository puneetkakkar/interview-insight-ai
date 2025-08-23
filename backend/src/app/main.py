from fastapi import FastAPI

from src.app.api.v1 import agent
from src.app.core.setup import create_application
from src.app.core.response import build_success_response

# Create the FastAPI application
app = create_application()

# Include API routers
app.include_router(agent.router, prefix="/api/v1")


# Add root endpoint
@app.get("/")
async def root() -> dict[str, object]:
    """Root endpoint with basic information."""
    return build_success_response(
        {
            "message": "FRAI Boilerplate",
            "version": "0.1.0",
            "docs": "/docs",
            "health": "/health",
        }
    )


# Add info endpoint
@app.get("/info")
async def info() -> dict[str, object]:
    """Application information endpoint."""
    return build_success_response(
        {
            "name": "FRAI Boilerplate",
            "description": "A production-ready FRAI boilerplate",
            "version": "0.1.0",
            "status": "running",
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
