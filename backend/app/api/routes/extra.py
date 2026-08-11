from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.dependencies import CurrentUser, DatabaseDependency
from app.repositories.org_repository import MongoOrgRepository
from app.schemas.extra import (
    AppCreateRequest,
    AppResponse,
    AppUpdateRequest,
    AutomationCreateRequest,
    AutomationResponse,
    AutomationUpdateRequest,
    MemberReportQueryRequest,
    OrgMemberInviteRequest,
    OrgMemberSearchRequest,
    PasswordUpdateRequest,
    PointCreateRequest,
    PointResponse,
    PointUpdateRequest,
    ProfileResponse,
    ProfileUpdateRequest,
    ReportQueryRequest,
    SchedulerCreateRequest,
    SchedulerResponse,
    StorageFileResponse,
    StoragePresignedUrlRequest,
    StorageSaveToDriveRequest,
    TimerLogResponse,
    TimerStartRequest,
    TimerStopRequest,
)
from app.services.extra_service import ExtraService

router = APIRouter(tags=["extra"])


def _get_service(database: DatabaseDependency) -> ExtraService:
    return ExtraService(database, MongoOrgRepository(database))


# ── Automation ────────────────────────────────────────────────────────────


@router.get("/automation", response_model=list[AutomationResponse])
async def get_automations(
    projectId: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[AutomationResponse]:
    return await _get_service(database).get_automations(projectId)


@router.post(
    "/automation",
    response_model=AutomationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_automation(
    data: AutomationCreateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> AutomationResponse:
    return await _get_service(database).create_automation(data, current_user.id)


@router.put("/automation", response_model=AutomationResponse)
async def update_automation(
    data: AutomationUpdateRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> AutomationResponse:
    return await _get_service(database).update_automation(data)


@router.delete("/automation")
async def delete_automation(
    id: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).delete_automation(id)
    return {"status": "ok"}


# ── Timer ─────────────────────────────────────────────────────────────────


@router.post("/timer/start", response_model=TimerLogResponse)
async def start_timer(
    data: TimerStartRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> TimerLogResponse:
    return await _get_service(database).start_timer(data, current_user.id)


@router.post("/timer/stop", response_model=TimerLogResponse)
async def stop_timer(
    data: TimerStopRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> TimerLogResponse:
    return await _get_service(database).stop_timer(data, current_user.id)


@router.get("/timer/current", response_model=TimerLogResponse | None)
async def get_current_timer(
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> TimerLogResponse | None:
    return await _get_service(database).get_current_timer(current_user.id)


@router.get("/timer/logs/{task_id}", response_model=list[TimerLogResponse])
async def get_timer_logs(
    task_id: str,
    page: int = 1,
    limit: int = 7,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[TimerLogResponse]:
    return await _get_service(database).get_timer_logs(task_id, page, limit)


# ── Scheduler ─────────────────────────────────────────────────────────────


@router.get("/scheduler/{project_id}", response_model=list[SchedulerResponse])
async def get_schedulers(
    project_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[SchedulerResponse]:
    return await _get_service(database).get_schedulers(project_id)


@router.post(
    "/scheduler",
    response_model=SchedulerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_scheduler(
    data: SchedulerCreateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> SchedulerResponse:
    return await _get_service(database).create_scheduler(data, current_user.id)


@router.delete("/scheduler/{sched_id}")
async def delete_scheduler(
    sched_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).delete_scheduler(sched_id)
    return {"status": "ok"}


# ── Meeting ───────────────────────────────────────────────────────────────


@router.get("/meeting/rooms")
async def get_meeting_rooms(
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[dict[str, object]]:
    return await _get_service(database).get_rooms()


@router.post("/meeting/room")
async def create_meeting_room(
    name: Annotated[str, Query()],
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return await _get_service(database).create_room(name, current_user.id)


@router.delete("/meeting/room/{name}")
async def delete_meeting_room(
    name: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).delete_room(name)
    return {"status": "ok"}


# ── Storage ───────────────────────────────────────────────────────────────


@router.post("/storage/create-presigned-url")
async def create_presigned_url(
    data: StoragePresignedUrlRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return await _get_service(database).create_presigned_url(data, current_user.id)


@router.get("/storage/get-files", response_model=list[StorageFileResponse])
async def get_files(
    ids: Annotated[list[str], Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[StorageFileResponse]:
    return await _get_service(database).get_files(ids)


@router.delete("/storage/del-file")
async def delete_file(
    id: Annotated[str, Query()],
    orgId: Annotated[str, Query()],
    projectId: Annotated[str, Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).delete_file(id)
    return {"status": "ok"}


@router.post("/storage/save-to-drive", response_model=StorageFileResponse)
async def save_to_drive(
    data: StorageSaveToDriveRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> StorageFileResponse:
    return await _get_service(database).save_to_drive(data, current_user.id)


# ── Report ────────────────────────────────────────────────────────────────


@router.post("/report/project")
async def get_project_report(
    data: ReportQueryRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, object]:
    return await _get_service(database).get_project_report(data)


@router.post("/report/members")
async def get_member_report(
    data: MemberReportQueryRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, object]:
    return await _get_service(database).get_member_report(data)


# ── Profile ───────────────────────────────────────────────────────────────


@router.get("/profile", response_model=ProfileResponse)
async def get_profile(
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> ProfileResponse:
    return await _get_service(database).get_profile(current_user.id)


@router.put("/profile", response_model=ProfileResponse)
async def update_profile(
    data: ProfileUpdateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> ProfileResponse:
    return await _get_service(database).update_profile(data, current_user.id)


@router.put("/profile/password")
async def update_password(
    data: PasswordUpdateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> dict[str, str]:
    await _get_service(database).update_password(data, current_user.id)
    return {"status": "ok"}


# ── Org Member ────────────────────────────────────────────────────────────


@router.get("/org/member/{org_id}")
async def get_org_members(
    org_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[dict[str, object]]:
    return await _get_service(database).get_org_members(org_id)


@router.post("/org/member/search")
async def search_org_members(
    data: OrgMemberSearchRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[dict[str, object]]:
    return await _get_service(database).search_org_members(data)


@router.post("/org/member/invite")
async def invite_org_member(
    data: OrgMemberInviteRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> dict[str, object]:
    return await _get_service(database).invite_org_member(data, current_user.id)


@router.delete("/org/member/remove/{org_id}/{uid}")
async def remove_org_member(
    org_id: str,
    uid: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).remove_org_member(org_id, uid)
    return {"status": "ok"}


# ── Apps ──────────────────────────────────────────────────────────────────


@router.get("/apps/{org_id}", response_model=list[AppResponse])
async def get_apps(
    org_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[AppResponse]:
    return await _get_service(database).get_apps(org_id)


@router.post(
    "/apps",
    response_model=AppResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_app(
    data: AppCreateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> AppResponse:
    return await _get_service(database).create_app(data, current_user.id)


@router.put("/apps", response_model=AppResponse)
async def update_app(
    data: AppUpdateRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> AppResponse:
    return await _get_service(database).update_app(data)


@router.delete("/apps/{app_id}")
async def delete_app(
    app_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).delete_app(app_id)
    return {"status": "ok"}


# ── Project Point ─────────────────────────────────────────────────────────


@router.get("/project/point/{project_id}", response_model=list[PointResponse])
async def get_points(
    project_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[PointResponse]:
    return await _get_service(database).get_points(project_id)


@router.post(
    "/project/point",
    response_model=PointResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_point(
    data: PointCreateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> PointResponse:
    return await _get_service(database).create_point(data, current_user.id)


@router.put("/project/point", response_model=PointResponse)
async def update_point(
    data: PointUpdateRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> PointResponse:
    return await _get_service(database).update_point(data)


@router.delete("/project/point/{point_id}")
async def delete_point(
    point_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).delete_point(point_id)
    return {"status": "ok"}


# ── Tag ───────────────────────────────────────────────────────────────────


@router.get("/project/tag/{project_id}")
async def get_tags(
    project_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[dict[str, object]]:
    return await _get_service(database).get_tags(project_id)