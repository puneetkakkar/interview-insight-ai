from fastapi import FastAPI
from datetime import datetime

from src.app.api.v1 import agent, transcript
from src.app.core.setup import create_application
from src.app.core.response import build_success_response
from src.app.core import settings

# Create the FastAPI application
app = create_application()

# Include API routers
app.include_router(agent.router, prefix="/api/v1")
app.include_router(transcript.router, prefix="/api/v1")


# Add root endpoint
@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "success": True,
        "message": "Interview Insight AI",
        "data": {
            "service": "Interview Insight AI",
            "version": "1.0.0",
            "status": "running",
            "timestamp": datetime.utcnow().isoformat(),
        },
    }


# Add info endpoint
@app.get("/info")
async def get_info():
    """Get detailed application information."""
    return {
        "success": True,
        "message": "Application information retrieved successfully",
        "data": {
            "name": "Interview Insight AI",
            "description": "A production-ready AI-powered interview transcript analysis platform",
            "version": "1.0.0",
            "environment": settings.environment,
            "storage_type": settings.storage_type,
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
            "ai_models": settings.available_models,
            "timestamp": datetime.utcnow().isoformat(),
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
