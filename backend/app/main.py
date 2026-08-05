from fastapi import FastAPI

from app.api.router import api_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="Namviek Python Rebuild API",
        version="0.1.0",
        description="Unofficial learning-oriented rebuild of the Namviek backend",
    )
    application.include_router(api_router, prefix="/api/v1")
    return application


app = create_app()

