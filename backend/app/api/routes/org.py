from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.dependencies import CurrentUser, DatabaseDependency
from app.repositories.org_repository import MongoOrgRepository
from app.schemas.org import (
    DashboardComponentCreateRequest,
    DashboardComponentResponse,
    DashboardCreateRequest,
    DashboardLayoutUpdateRequest,
    DashboardResponse,
    FavoriteCreateRequest,
    FavoriteResponse,
    FieldCreateRequest,
    FieldResponse,
    FieldSortableRequest,
    FieldUpdateRequest,
    OrgCreateRequest,
    OrgResponse,
    OrgStorageResponse,
    OrgStorageUpdateRequest,
    OrgUpdateRequest,
    VisionCreateRequest,
    VisionResponse,
    VisionUpdateRequest,
)
from app.services.org_service import OrgService

router = APIRouter(tags=["org"])


def _get_service(database: DatabaseDependency) -> OrgService:
    return OrgService(MongoOrgRepository(database))


# ── Organization ──────────────────────────────────────────────────────────


@router.get("/org", response_model=list[OrgResponse])
async def get_orgs(
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> list[OrgResponse]:
    return await _get_service(database).get_orgs(current_user.id)


@router.get("/org/query/slug", response_model=OrgResponse)
async def get_org_by_slug(
    slug: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> OrgResponse:
    return await _get_service(database).get_org_by_slug(slug)


@router.get("/org/{org_id}", response_model=OrgResponse)
async def get_org_by_id(
    org_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> OrgResponse:
    return await _get_service(database).get_org_by_id(org_id)


@router.post(
    "/org", response_model=OrgResponse, status_code=status.HTTP_201_CREATED
)
async def create_org(
    data: OrgCreateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> OrgResponse:
    return await _get_service(database).create_org(data, current_user.id)


@router.put("/org", response_model=OrgResponse)
async def update_org(
    data: OrgUpdateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> OrgResponse:
    return await _get_service(database).update_org(data, current_user.id)


# ── Org Storage ───────────────────────────────────────────────────────────


@router.get("/org-storage", response_model=OrgStorageResponse | None)
async def get_org_storage(
    orgId: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> OrgStorageResponse | None:
    return await _get_service(database).get_org_storage(orgId)


@router.put("/org-storage", response_model=OrgStorageResponse)
async def update_org_storage(
    data: OrgStorageUpdateRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> OrgStorageResponse:
    return await _get_service(database).update_org_storage(data)


# ── Member ────────────────────────────────────────────────────────────────


@router.get("/project/member")
async def get_members(
    projectId: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[dict[str, object]]:
    return await _get_service(database).get_members(projectId)


@router.post("/project/member")
async def add_members(
    projectId: Annotated[str, Query()],
    members: list[dict[str, object]],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[dict[str, object]]:
    return await _get_service(database).add_members(projectId, members)


@router.put("/project/member/role")
async def update_member_role(
    uid: Annotated[str, Query()],
    projectId: Annotated[str, Query()],
    role: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, object]:
    return await _get_service(database).update_member_role(uid, projectId, role)


@router.delete("/project/member")
async def remove_member(
    projectId: Annotated[str, Query()],
    uid: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).remove_member(uid, projectId)
    return {"status": "ok"}


# ── Favorite ──────────────────────────────────────────────────────────────


@router.get("/favorite", response_model=list[FavoriteResponse])
async def get_favorites(
    orgId: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[FavoriteResponse]:
    return await _get_service(database).get_favorites(orgId)


@router.post(
    "/favorite",
    response_model=FavoriteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_favorite(
    data: FavoriteCreateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> FavoriteResponse:
    return await _get_service(database).create_favorite(data, current_user.id)


@router.delete("/favorite")
async def delete_favorite(
    id: Annotated[str, Query()],
    orgId: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).delete_favorite(id)
    return {"status": "ok"}


# ── Vision ────────────────────────────────────────────────────────────────


@router.get("/vision/get-by-project", response_model=list[VisionResponse])
async def get_visions_by_project(
    projectId: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[VisionResponse]:
    return await _get_service(database).get_visions_by_project(projectId)


@router.get("/vision/get-by-org", response_model=list[VisionResponse])
async def get_visions_by_org(
    orgId: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[VisionResponse]:
    return await _get_service(database).get_visions_by_org(orgId)


@router.post(
    "/vision",
    response_model=VisionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_vision(
    data: VisionCreateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> VisionResponse:
    return await _get_service(database).create_vision(data, current_user.id)


@router.put("/vision", response_model=VisionResponse)
async def update_vision(
    data: VisionUpdateRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> VisionResponse:
    return await _get_service(database).update_vision(data)


@router.delete("/vision/{vision_id}")
async def delete_vision(
    vision_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).delete_vision(vision_id)
    return {"status": "ok"}


# ── Dashboard ─────────────────────────────────────────────────────────────


@router.get("/dboard", response_model=list[DashboardResponse])
async def get_dashboards(
    projectId: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[DashboardResponse]:
    return await _get_service(database).get_dashboards(projectId)


@router.post(
    "/dboard",
    response_model=DashboardResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_dashboard(
    data: DashboardCreateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> DashboardResponse:
    return await _get_service(database).create_dashboard(data, current_user.id)


@router.get("/dboard/components", response_model=list[DashboardComponentResponse])
async def get_dboard_components(
    dboardId: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[DashboardComponentResponse]:
    return await _get_service(database).get_dboard_components(dboardId)


@router.post(
    "/dboard/component",
    response_model=DashboardComponentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_dboard_component(
    data: DashboardComponentCreateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> DashboardComponentResponse:
    return await _get_service(database).create_dboard_component(data, current_user.id)


@router.delete("/dboard/component")
async def delete_dboard_component(
    componentId: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).delete_dboard_component(componentId)
    return {"status": "ok"}


@router.post("/dboard/update-layout")
async def update_dboard_layout(
    data: DashboardLayoutUpdateRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).update_dboard_layout(data)
    return {"status": "ok"}


# ── Custom Field ──────────────────────────────────────────────────────────


@router.get("/fields/{project_id}", response_model=list[FieldResponse])
async def get_fields(
    project_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[FieldResponse]:
    return await _get_service(database).get_fields(project_id)


@router.post(
    "/fields",
    response_model=FieldResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_field(
    data: FieldCreateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> FieldResponse:
    return await _get_service(database).create_field(data, current_user.id)


@router.put("/fields", response_model=FieldResponse)
async def update_field(
    data: FieldUpdateRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> FieldResponse:
    return await _get_service(database).update_field(data)


@router.put("/fields/sortable")
async def sort_fields(
    data: FieldSortableRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).sort_fields(data)
    return {"status": "ok"}


@router.delete("/fields/{field_id}")
async def delete_field(
    field_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).delete_field(field_id)
    return {"status": "ok"}