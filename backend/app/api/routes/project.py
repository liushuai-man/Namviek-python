from fastapi import APIRouter, Query, status

from app.api.dependencies import CurrentUser, DatabaseDependency
from app.repositories.project_repository import MongoProjectRepository
from app.schemas.project import (
    ProjectArchiveRequest,
    ProjectCreateRequest,
    ProjectPinRequest,
    ProjectResponse,
    ProjectStatusCreateRequest,
    ProjectStatusOrderRequest,
    ProjectStatusResponse,
    ProjectStatusUpdateRequest,
    ProjectUpdateRequest,
    ProjectViewCreateRequest,
    ProjectViewResponse,
    ProjectViewUpdateRequest,
)
from app.services.project_service import ProjectService

router = APIRouter(prefix="/project", tags=["project"])


def _get_service(database: DatabaseDependency) -> ProjectService:
    return ProjectService(MongoProjectRepository(database))


# ── Project CRUD ─────────────────────────────────────────────────────


@router.get("", response_model=list[ProjectResponse])
async def get_projects(
    orgId: str = Query(..., description="Organization ID"),
    isArchived: bool = Query(False),
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[ProjectResponse]:
    service = _get_service(database)
    return await service.get_projects(orgId, is_archived=isArchived)


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> ProjectResponse:
    service = _get_service(database)
    return await service.create_project(data, current_user.id)


@router.put("", response_model=ProjectResponse)
async def update_project(
    data: ProjectUpdateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> ProjectResponse:
    service = _get_service(database)
    return await service.update_project(data, current_user.id)


@router.post("/archive", response_model=ProjectResponse)
async def archive_project(
    data: ProjectArchiveRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> ProjectResponse:
    service = _get_service(database)
    return await service.archive_project(data.projectId, data.archive, current_user.id)


@router.post("/pin")
async def pin_project(
    data: ProjectPinRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> dict[str, str]:
    return {"status": "ok"}


@router.delete("/pin")
async def unpin_project(
    projectId: str = Query(...),
    current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, str]:
    return {"status": "ok"}


@router.get("/pin")
async def get_pinned_projects(
    current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> list[dict[str, object]]:
    return []


# ── Status ───────────────────────────────────────────────────────────


@router.get("/status/{project_id}", response_model=list[ProjectStatusResponse])
async def get_statuses(
    project_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[ProjectStatusResponse]:
    service = _get_service(database)
    return await service.get_statuses(project_id)


@router.post(
    "/status/{project_id}",
    response_model=ProjectStatusResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_status(
    project_id: str,
    data: ProjectStatusCreateRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> ProjectStatusResponse:
    service = _get_service(database)
    data.projectId = project_id
    return await service.create_status(data)


@router.put("/status/order")
async def update_status_order(
    data: ProjectStatusOrderRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    service = _get_service(database)
    await service.update_status_order(data)
    return {"status": "ok"}


@router.put("/status", response_model=ProjectStatusResponse)
async def update_status(
    data: ProjectStatusUpdateRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> ProjectStatusResponse:
    service = _get_service(database)
    return await service.update_status(data)


@router.delete("/status/{status_id}")
async def delete_status(
    status_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    service = _get_service(database)
    await service.delete_status(status_id)
    return {"status": "ok"}


# ── View ─────────────────────────────────────────────────────────────


@router.get("/project-view", response_model=list[ProjectViewResponse])
async def get_views(
    projectId: str = Query(...),
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[ProjectViewResponse]:
    service = _get_service(database)
    return await service.get_views(projectId)


@router.get("/project-view/{view_id}", response_model=ProjectViewResponse)
async def get_view(
    view_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> ProjectViewResponse:
    service = _get_service(database)
    return await service.get_view(view_id)


@router.post(
    "/project-view",
    response_model=ProjectViewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_view(
    data: ProjectViewCreateRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> ProjectViewResponse:
    service = _get_service(database)
    return await service.create_view(data)


@router.put("/project-view", response_model=ProjectViewResponse)
async def update_view(
    data: ProjectViewUpdateRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> ProjectViewResponse:
    service = _get_service(database)
    return await service.update_view(data)


@router.delete("/project-view")
async def delete_view(
    id: str = Query(...),
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    service = _get_service(database)
    await service.delete_view(id)
    return {"status": "ok"}