from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.dependencies import CurrentUser, DatabaseDependency
from app.repositories.task_repository import MongoTaskRepository
from app.schemas.task import (
    ActivityCreateRequest,
    ActivityResponse,
    ActivityUpdateRequest,
    ChecklistCreateRequest,
    ChecklistResponse,
    ChecklistUpdateRequest,
    CommentCreateRequest,
    CommentResponse,
    CommentUpdateRequest,
    TaskAddManyRequest,
    TaskCreateRequest,
    TaskQueryRequest,
    TaskReorderRequest,
    TaskResponse,
    TaskUpdateManyRequest,
    TaskUpdateRequest,
)
from app.services.task_service import TaskService

router = APIRouter(tags=["task"])


def _get_service(database: DatabaseDependency) -> TaskService:
    return TaskService(MongoTaskRepository(database))


# ── Task CRUD ─────────────────────────────────────────────────────────


@router.get("/project/task", response_model=list[TaskResponse])
async def get_tasks(
    projectId: str = Query(...),
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[TaskResponse]:
    return await _get_service(database).get_tasks(projectId)


@router.get("/project/task/query", response_model=list[TaskResponse])
async def query_tasks(
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
    projectId: Annotated[str | None, Query()] = None,
    projectIds: Annotated[list[str] | None, Query()] = None,
    title: Annotated[str | None, Query()] = None,
    statusIds: Annotated[list[str] | None, Query()] = None,
    assigneeIds: Annotated[list[str] | None, Query()] = None,
    priority: Annotated[str | None, Query()] = None,
    done: Annotated[str | None, Query()] = None,
    take: Annotated[int | None, Query()] = None,
    skip: Annotated[int | None, Query()] = None,
) -> list[TaskResponse]:
    query = TaskQueryRequest(
        projectId=projectId,
        projectIds=projectIds,
        title=title,
        statusIds=statusIds,
        assigneeIds=assigneeIds,
        priority=priority,
        done=done,
        take=take,
        skip=skip,
    )
    return await _get_service(database).query_tasks(query)


@router.get("/project/task/counter")
async def task_counter(
    projectIds: Annotated[list[str] | None, Query()] = None,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[dict[str, object]]:
    if not projectIds:
        return []
    try:
        return await _get_service(database).get_counter(projectIds)
    except Exception:
        return []


@router.post(
    "/project/task", response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
async def create_task(
    data: TaskCreateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> TaskResponse:
    return await _get_service(database).create_task(data, current_user.id)


@router.put("/project/task", response_model=TaskResponse)
async def update_task(
    data: TaskUpdateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> TaskResponse:
    return await _get_service(database).update_task(data, current_user.id)


@router.put("/project/task-many")
async def update_many_tasks(
    data: TaskUpdateManyRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> dict[str, int]:
    return await _get_service(database).update_many_tasks(data, current_user.id)


@router.delete("/project/task")
async def delete_task(
    projectId: str = Query(...),
    id: str = Query(...),
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).delete_task(id)
    return {"status": "ok"}


@router.delete("/project/tasks")
async def delete_many_tasks(
    projectId: Annotated[str, Query()],
    ids: Annotated[list[str], Query()],
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, int]:
    return await _get_service(database).delete_many_tasks(ids)


@router.post("/project/tasks", response_model=list[TaskResponse])
async def create_many_tasks(
    data: TaskAddManyRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> list[TaskResponse]:
    return await _get_service(database).create_many_tasks(data, current_user.id)


@router.post("/task/reorder")
async def reorder_tasks(
    data: TaskReorderRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).reorder_tasks(data)
    return {"status": "ok"}


@router.post("/project/task/make-cover", response_model=TaskResponse)
async def make_cover(
    taskId: str = Query(...),
    url: str = Query(...),
    projectId: str = Query(...),
    current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> TaskResponse:
    return await _get_service(database).make_cover(taskId, url, current_user.id)


# ── Checklist ─────────────────────────────────────────────────────────


@router.get(
    "/project/task/checklist/{task_id}", response_model=list[ChecklistResponse]
)
async def get_checklists(
    task_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[ChecklistResponse]:
    return await _get_service(database).get_checklists(task_id)


@router.post(
    "/project/task/checklist",
    response_model=ChecklistResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_checklist(
    data: ChecklistCreateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> ChecklistResponse:
    return await _get_service(database).create_checklist(data, current_user.id)


@router.put("/project/task/checklist", response_model=ChecklistResponse)
async def update_checklist(
    data: ChecklistUpdateRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> ChecklistResponse:
    return await _get_service(database).update_checklist(data)


@router.delete("/project/task/checklist/{checklist_id}")
async def delete_checklist(
    checklist_id: str,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).delete_checklist(checklist_id)
    return {"status": "ok"}


# ── Comment ───────────────────────────────────────────────────────────


@router.get("/comment", response_model=list[CommentResponse])
async def get_comments(
    taskId: str = Query(...),
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[CommentResponse]:
    return await _get_service(database).get_comments(taskId)


@router.post(
    "/comment",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    data: CommentCreateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> CommentResponse:
    return await _get_service(database).create_comment(data, current_user.id)


@router.put("/comment", response_model=CommentResponse)
async def update_comment(
    data: CommentUpdateRequest,
    current_user: CurrentUser,
    database: DatabaseDependency = None,
) -> CommentResponse:
    return await _get_service(database).update_comment(data, current_user.id)


@router.delete("/comment")
async def delete_comment(
    id: str = Query(...),
    taskId: str = Query(...),
    updatedBy: str = Query(...),
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).delete_comment(id)
    return {"status": "ok"}


# ── Activity ──────────────────────────────────────────────────────────


@router.get("/activity", response_model=list[ActivityResponse])
async def get_activities(
    objectId: str = Query(...),
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> list[ActivityResponse]:
    return await _get_service(database).get_activities(objectId)


@router.post(
    "/activity",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_activity(
    data: ActivityCreateRequest,
    objectId: str = Query(...),
    current_user: CurrentUser = None,
    database: DatabaseDependency = None,
) -> ActivityResponse:
    return await _get_service(database).create_activity(data, objectId, current_user.id)


@router.put("/activity", response_model=ActivityResponse)
async def update_activity(
    data: ActivityUpdateRequest,
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> ActivityResponse:
    return await _get_service(database).update_activity(data)


@router.delete("/activity")
async def delete_activity(
    id: str = Query(...),
    database: DatabaseDependency = None,
    _current_user: CurrentUser = None,
) -> dict[str, str]:
    await _get_service(database).delete_activity(id)
    return {"status": "ok"}