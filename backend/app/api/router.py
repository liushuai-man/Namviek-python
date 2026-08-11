from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.extra import router as extra_router
from app.api.routes.health import router as health_router
from app.api.routes.org import router as org_router
from app.api.routes.project import router as project_router
from app.api.routes.task import router as task_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(project_router)
api_router.include_router(task_router)
api_router.include_router(org_router)
api_router.include_router(extra_router)
