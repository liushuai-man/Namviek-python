from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.dependencies import CurrentUser, DatabaseDependency
from app.repositories.project_repository import MongoProjectRepository
from app.repositories.task_repository import MongoTaskRepository
from app.schemas.org import (
    FieldCreateRequest,
    FieldResponse,
    FieldSortableRequest,
    FieldUpdateRequest,
)
from app.schemas.project import (
    ProjectPointCreateRequest,
    ProjectPointResponse,
    ProjectPointUpdateRequest,
    ProjectResponse,
    ProjectTagCreateRequest,
    ProjectTagResponse,
    ProjectTagUpdateRequest,
    ProjectViewCreateRequest,
    ProjectViewResponse,
    ProjectViewUpdateRequest,
)
from app.schemas.task import TaskReorderRequest
from app.services.project_service import ProjectService
from app.services.task_service import TaskService

router = APIRouter(tags=["frontend_compat"])


def _get_project_service(database: DatabaseDependency) -> ProjectService:
    return ProjectService(MongoProjectRepository(database))


def _get_task_service(database: DatabaseDependency) -> TaskService:
    return TaskService(MongoTaskRepository(database))


# ── Project View (frontend path: /api/project-view) ──────────────────


@router.get("/project-view", response_model=list[ProjectViewResponse])
async def get_views(
    projectId: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[ProjectViewResponse]:
    service = _get_project_service(database)
    return await service.get_views(projectId)


@router.get("/project-view/{view_id}", response_model=ProjectViewResponse)
async def get_view(
    view_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> ProjectViewResponse:
    service = _get_project_service(database)
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
    service = _get_project_service(database)
    return await service.create_view(data)


@router.put("/project-view", response_model=ProjectViewResponse)
async def update_view(
    data: ProjectViewUpdateRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> ProjectViewResponse:
    service = _get_project_service(database)
    return await service.update_view(data)


@router.delete("/project-view")
async def delete_view(
    id: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    service = _get_project_service(database)
    await service.delete_view(id)
    return {"status": "ok"}


# ── Event routes (frontend path: /api/event) ──────────────────────────


@router.post("/event/task-reorder")
async def task_reorder_event(
    data: TaskReorderRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    service = _get_task_service(database)
    await service.reorder_tasks(data)
    return {"status": "ok"}


@router.post("/event/task-move-to-other-board")
async def task_move_event(
    data: dict[str, object],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    return {"status": "ok"}


# ── Project Grid (frontend path: /api/project/grid) ───────────────────


@router.post("/project/grid/query")
async def grid_query(
    data: dict[str, object],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, object]:
    return {"items": [], "total": 0}


@router.post("/project/grid/create")
async def grid_create(
    data: dict[str, object],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return {"status": "ok"}


@router.put("/project/grid")
async def grid_update(
    data: dict[str, object],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return {"status": "ok"}


@router.put("/project/grid/update-many")
async def grid_update_many(
    data: dict[str, object],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return {"status": "ok"}


@router.delete("/project/grid/delete")
async def grid_delete(
    data: dict[str, object],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return {"status": "ok"}


# ── Project Settings (frontend path: /api/project-setting) ────────────


@router.put("/project-setting/daily-report")
async def update_daily_report(
    data: dict[str, object],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return {"status": "ok"}


@router.get("/project-setting/daily-report/{project_id}")
async def get_daily_report(
    project_id: str,
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return {"enabled": False, "time": "09:00"}


@router.put("/project-setting/notification")
async def update_notification(
    data: dict[str, object],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return {"status": "ok"}


@router.get("/project-setting/notification")
async def get_notification(
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return {"email": True, "push": True}


# ── Task export & custom query ────────────────────────────────────────


@router.get("/project/task/export")
async def export_tasks(
    projectId: Annotated[str, Query()],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> list[dict[str, object]]:
    try:
        service = _get_task_service(database)
        tasks = await service.get_tasks(projectId)
        return [t.model_dump() for t in tasks]
    except Exception as e:
        print(f"Export error: {e}")
        return []


@router.post("/project/task/custom-field/query")
async def custom_field_query(
    data: dict[str, object],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return {"items": [], "total": 0}


# ── Storage get-object-url ────────────────────────────────────────────


@router.get("/storage/get-object-url")
async def get_object_url(
    id: Annotated[str, Query()],
    orgId: Annotated[str, Query()],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return {"url": "", "expiresAt": None}


# ── Meeting participants ─────────────────────────────────────────────


@router.get("/meeting/get-participants")
async def get_meeting_participants(
    roomId: Annotated[str, Query()],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> list[dict[str, object]]:
    return []


# ── Dashboard query endpoints ─────────────────────────────────────────


@router.post("/dboard/query-summary")
async def query_dashboard_summary(
    data: dict[str, object],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return {"total": 0, "completed": 0, "overdue": 0}


@router.post("/dboard/query-column")
async def query_dashboard_column(
    data: dict[str, object],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> list[dict[str, object]]:
    return []


@router.post("/dboard/query-burnchart/{chart_type}")
async def query_burnchart(
    chart_type: str,
    data: dict[str, object],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> list[dict[str, object]]:
    return []


# ── Private sign-up ───────────────────────────────────────────────────


@router.post("/auth/sign-up-private", status_code=status.HTTP_201_CREATED)
async def sign_up_private(
    data: dict[str, object],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return {"status": 201, "data": {}}


# ── Project Point (frontend path: /api/project/point) ────────────────


@router.get("/project/point/{project_id}", response_model=list[ProjectPointResponse])
async def get_project_points(
    project_id: str,
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> list[ProjectPointResponse]:
    return []


@router.post(
    "/project/point",
    response_model=ProjectPointResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project_point(
    data: ProjectPointCreateRequest,
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> ProjectPointResponse:
    return ProjectPointResponse(
        id="",
        name=data.name,
        value=data.value,
        icon=data.icon,
        order=data.order,
        projectId=data.projectId,
        createdAt=__import__("datetime").datetime.now(),
    )


@router.put("/project/point", response_model=ProjectPointResponse)
async def update_project_point(
    data: ProjectPointUpdateRequest,
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> ProjectPointResponse:
    return ProjectPointResponse(
        id=data.id,
        name=data.name or "",
        value="",
        icon=data.icon,
        order=data.order or 0,
        projectId="",
        createdAt=__import__("datetime").datetime.now(),
    )


@router.delete("/project/point/{point_id}")
async def delete_project_point(
    point_id: str,
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, str]:
    return {"status": "ok"}


# ── Project Tag (frontend path: /api/project/tag) ────────────────────


@router.get("/project/tag/{project_id}", response_model=list[ProjectTagResponse])
async def get_project_tags(
    project_id: str,
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> list[ProjectTagResponse]:
    return []


@router.post(
    "/project/tag",
    response_model=ProjectTagResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project_tag(
    data: ProjectTagCreateRequest,
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> ProjectTagResponse:
    return ProjectTagResponse(
        id="",
        name=data.name,
        color=data.color,
        projectId=data.projectId,
        createdAt=__import__("datetime").datetime.now(),
    )


@router.put("/project/tag", response_model=ProjectTagResponse)
async def update_project_tag(
    data: ProjectTagUpdateRequest,
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> ProjectTagResponse:
    return ProjectTagResponse(
        id=data.id,
        name=data.name or "",
        color=data.color,
        projectId="",
        createdAt=__import__("datetime").datetime.now(),
    )


# ── Fields (frontend path: /api/fields) ──────────────────────────────


@router.get("/fields/{project_id}", response_model=list[FieldResponse])
async def get_fields(
    project_id: str,
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> list[FieldResponse]:
    return []


@router.post(
    "/fields",
    response_model=FieldResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_field(
    data: FieldCreateRequest,
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> FieldResponse:
    return FieldResponse(
        id="",
        name=data.name,
        type=data.type,
        icon=data.icon,
        order=data.order,
        visible=data.visible,
        projectId=data.projectId,
        createdBy="",
        createdAt=__import__("datetime").datetime.now(),
    )


@router.put("/fields", response_model=FieldResponse)
async def update_field(
    data: FieldUpdateRequest,
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> FieldResponse:
    return FieldResponse(
        id=data.id,
        name=data.name or "",
        type="",
        icon=data.icon,
        order=data.order or 0,
        visible=True,
        projectId="",
        createdBy="",
        createdAt=__import__("datetime").datetime.now(),
    )


@router.delete("/fields/{field_id}")
async def delete_field(
    field_id: str,
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, str]:
    return {"status": "ok"}


@router.put("/fields/sortable")
async def sort_fields(
    data: FieldSortableRequest,
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, str]:
    return {"status": "ok"}


# ── Organization routes (frontend path: /api/org-storage) ────────────


@router.get("/org-storage")
async def get_org_storage(
    orgId: Annotated[str, Query()],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return {"type": "LOCAL", "config": {}}


@router.put("/org-storage")
async def update_org_storage(
    data: dict[str, object],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, str]:
    return {"status": "ok"}


@router.get("/org/query/slug")
async def get_org_by_slug(
    slug: Annotated[str, Query()],
    _current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return {}
