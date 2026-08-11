from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.api.routes.auth import router as auth_router
from app.api.routes.extra import router as extra_router
from app.api.routes.org import router as org_router
from app.api.routes.project import router as project_router
from app.api.routes.task import router as task_router
from app.core.config import get_settings
from app.core.errors import AppError
from app.core.exception_handlers import app_error_handler
from app.core.middleware import SecurityHeadersMiddleware
from app.db.mongodb import lifespan


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="Namviek Python Rebuild API",
        version="0.1.0",
        description="Unofficial learning-oriented rebuild of the Namviek backend",
        lifespan=lifespan,
    )
    settings = get_settings()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Authorization", "RefreshToken"],
    )
    application.add_middleware(SecurityHeadersMiddleware)
    application.add_exception_handler(AppError, app_error_handler)
    application.include_router(api_router, prefix="/api/v1")
    # Temporary compatibility path used by the existing Next.js frontend.
    application.include_router(auth_router, prefix="/api", include_in_schema=False)
    application.include_router(project_router, prefix="/api", include_in_schema=False)
    application.include_router(task_router, prefix="/api", include_in_schema=False)
    application.include_router(org_router, prefix="/api", include_in_schema=False)
    application.include_router(extra_router, prefix="/api", include_in_schema=False)
    return application


app = create_app()
