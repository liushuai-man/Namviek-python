from bson import ObjectId

from app.core.errors import AppError
from app.models.task import (
    TaskActivityDocument,
    TaskChecklistDocument,
    TaskCommentDocument,
    TaskDocument,
)
from app.repositories.task_repository import TaskRepositoryProtocol
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


class TaskService:
    def __init__(self, repository: TaskRepositoryProtocol) -> None:
        self._repo = repository

    # ── Task CRUD ─────────────────────────────────────────────────────

    async def create_task(self, data: TaskCreateRequest, user_id: str) -> TaskResponse:
        task = await self._repo.create(
            title=data.title,
            desc=data.desc,
            projectId=ObjectId(data.projectId),
            statusId=ObjectId(data.statusId) if data.statusId else None,
            priority=data.priority,
            assigneeIds=[ObjectId(a) for a in data.assigneeIds],
            taskStatusId=ObjectId(data.taskStatusId) if data.taskStatusId else None,
            taskPointId=ObjectId(data.taskPointId) if data.taskPointId else None,
            dueDate=data.dueDate,
            startDate=data.startDate,
            done=data.done,
            order=data.order,
            tagIds=[ObjectId(t) for t in data.tagIds],
            createdBy=ObjectId(user_id),
        )
        return _to_task_response(task)

    async def get_tasks(self, project_id: str) -> list[TaskResponse]:
        tasks = await self._repo.find_by_project(project_id)
        return [_to_task_response(t) for t in tasks]

    async def query_tasks(self, query: TaskQueryRequest) -> list[TaskResponse]:
        project_ids = None
        if query.projectIds:
            project_ids = [ObjectId(pid) for pid in query.projectIds]
        elif query.projectId:
            project_ids = [ObjectId(query.projectId)]

        status_ids = [ObjectId(s) for s in query.statusIds] if query.statusIds else None
        assignee_ids = (
            [ObjectId(a) for a in query.assigneeIds] if query.assigneeIds else None
        )

        done = None
        if query.done == "yes":
            done = True
        elif query.done == "no":
            done = False

        order_by = None
        if query.orderBy:
            order_by = (query.orderBy[0], 1 if query.orderBy[1] == "asc" else -1)

        tasks = await self._repo.find_by_query(
            project_ids=project_ids,
            status_ids=status_ids,
            assignee_ids=assignee_ids,
            priority=query.priority,
            done=done,
            title=query.title,
            take=query.take,
            skip=query.skip,
            order_by=order_by,
        )
        return [_to_task_response(t) for t in tasks]

    async def update_task(
        self, data: TaskUpdateRequest, user_id: str
    ) -> TaskResponse:
        updates = _build_task_updates(data, user_id)
        task = await self._repo.update(ObjectId(data.id), updates)
        if not task:
            raise AppError(404, "not_found", "Task not found")
        return _to_task_response(task)

    async def update_many_tasks(
        self, data: TaskUpdateManyRequest, user_id: str
    ) -> dict[str, int]:
        ids = [ObjectId(i) for i in data.ids]
        updates = _build_task_updates(data.data, user_id)
        count = await self._repo.update_many(ids, updates)
        return {"updated": count}

    async def delete_task(self, task_id: str) -> None:
        deleted = await self._repo.delete(ObjectId(task_id))
        if not deleted:
            raise AppError(404, "not_found", "Task not found")

    async def delete_many_tasks(self, ids: list[str]) -> dict[str, int]:
        oids = [ObjectId(i) for i in ids]
        count = await self._repo.delete_many(oids)
        return {"deleted": count}

    async def create_many_tasks(
        self, data: TaskAddManyRequest, user_id: str
    ) -> list[TaskResponse]:
        tasks = []
        for item in data.data:
            task = await self._repo.create(
                title=item.title,
                desc=item.desc,
                projectId=ObjectId(data.projectId),
                statusId=ObjectId(item.statusId) if item.statusId else None,
                priority=item.priority,
                assigneeIds=[ObjectId(a) for a in item.assigneeIds],
                order=item.order,
                tagIds=[ObjectId(t) for t in item.tagIds],
                createdBy=ObjectId(user_id),
            )
            tasks.append(_to_task_response(task))
        return tasks

    async def reorder_tasks(self, data: TaskReorderRequest) -> None:
        orders: list[tuple[ObjectId, int]] = []
        for item in data.updatedOrder:
            oid = ObjectId(str(item[0]))
            order = int(item[1])
            orders.append((oid, order))
        await self._repo.update_order(orders)

    async def make_cover(
        self, task_id: str, url: str, _user_id: str
    ) -> TaskResponse:
        task = await self._repo.update(
            ObjectId(task_id), {"cover": url}
        )
        if not task:
            raise AppError(404, "not_found", "Task not found")
        return _to_task_response(task)

    async def get_counter(
        self, project_ids: list[str]
    ) -> list[dict[str, object]]:
        return await self._repo.count_by_status(project_ids)

    # ── Checklist ─────────────────────────────────────────────────────

    async def create_checklist(
        self, data: ChecklistCreateRequest, user_id: str
    ) -> ChecklistResponse:
        checklist = await self._repo.create_checklist(
            title=data.title,
            taskId=ObjectId(data.taskId),
            done=data.done,
            doneBy=ObjectId(data.doneBy) if data.doneBy else None,
            order=data.order,
            createdBy=ObjectId(user_id),
        )
        return _to_checklist_response(checklist)

    async def get_checklists(self, task_id: str) -> list[ChecklistResponse]:
        items = await self._repo.find_checklists_by_task(task_id)
        return [_to_checklist_response(c) for c in items]

    async def update_checklist(
        self, data: ChecklistUpdateRequest
    ) -> ChecklistResponse:
        updates: dict[str, object] = {}
        if data.title is not None:
            updates["title"] = data.title
        if data.done is not None:
            updates["done"] = data.done
            if data.done and data.doneBy:
                updates["doneBy"] = ObjectId(data.doneBy)
        if data.order is not None:
            updates["order"] = data.order
        item = await self._repo.update_checklist(ObjectId(data.id), updates)
        if not item:
            raise AppError(404, "not_found", "Checklist not found")
        return _to_checklist_response(item)

    async def delete_checklist(self, checklist_id: str) -> None:
        deleted = await self._repo.delete_checklist(ObjectId(checklist_id))
        if not deleted:
            raise AppError(404, "not_found", "Checklist not found")

    # ── Comment ───────────────────────────────────────────────────────

    async def create_comment(
        self, data: CommentCreateRequest, user_id: str
    ) -> CommentResponse:
        comment = await self._repo.create_comment(
            content=data.content,
            taskId=ObjectId(data.taskId),
            createdBy=ObjectId(user_id),
        )
        return _to_comment_response(comment)

    async def get_comments(self, task_id: str) -> list[CommentResponse]:
        comments = await self._repo.find_comments_by_task(task_id)
        return [_to_comment_response(c) for c in comments]

    async def update_comment(
        self, data: CommentUpdateRequest, user_id: str
    ) -> CommentResponse:
        updates: dict[str, object] = {"updatedBy": ObjectId(user_id)}
        if data.content is not None:
            updates["content"] = data.content
        comment = await self._repo.update_comment(ObjectId(data.id), updates)
        if not comment:
            raise AppError(404, "not_found", "Comment not found")
        return _to_comment_response(comment)

    async def delete_comment(self, comment_id: str) -> None:
        deleted = await self._repo.delete_comment(ObjectId(comment_id))
        if not deleted:
            raise AppError(404, "not_found", "Comment not found")

    # ── Activity ──────────────────────────────────────────────────────

    async def create_activity(
        self, data: ActivityCreateRequest, object_id: str, user_id: str
    ) -> ActivityResponse:
        activity = await self._repo.create_activity(
            objectId=ObjectId(object_id),
            type=data.type,
            data=data.data,
            createdBy=ObjectId(user_id),
        )
        return _to_activity_response(activity)

    async def get_activities(self, object_id: str) -> list[ActivityResponse]:
        activities = await self._repo.find_activities_by_object(object_id)
        return [_to_activity_response(a) for a in activities]

    async def update_activity(
        self, data: ActivityUpdateRequest
    ) -> ActivityResponse:
        updates: dict[str, object] = {}
        if data.data is not None:
            updates["data"] = data.data
        activity = await self._repo.update_activity(ObjectId(data.id), updates)
        if not activity:
            raise AppError(404, "not_found", "Activity not found")
        return _to_activity_response(activity)

    async def delete_activity(self, activity_id: str) -> None:
        deleted = await self._repo.delete_activity(ObjectId(activity_id))
        if not deleted:
            raise AppError(404, "not_found", "Activity not found")


# ── Helpers ────────────────────────────────────────────────────────────


def _build_task_updates(
    data: TaskUpdateRequest, user_id: str
) -> dict[str, object]:
    updates: dict[str, object] = {"updatedBy": ObjectId(user_id)}
    for field in (
        "title", "desc", "statusId", "priority", "dueDate",
        "startDate", "done", "order", "cover", "taskStatusId", "taskPointId",
    ):
        value = getattr(data, field, None)
        if value is not None:
            if field in ("statusId", "taskStatusId", "taskPointId"):
                updates[field] = ObjectId(str(value))
            else:
                updates[field] = value
    if data.assigneeIds is not None:
        updates["assigneeIds"] = [ObjectId(a) for a in data.assigneeIds]
    if data.tagIds is not None:
        updates["tagIds"] = [ObjectId(t) for t in data.tagIds]
    return updates


def _to_task_response(doc: TaskDocument) -> TaskResponse:
    return TaskResponse(
        id=str(doc["_id"]),
        title=doc["title"],
        desc=doc["desc"],
        projectId=str(doc["projectId"]),
        statusId=str(doc["statusId"]) if doc.get("statusId") else None,
        priority=doc.get("priority"),
        assigneeIds=[str(a) for a in doc.get("assigneeIds", [])],
        taskStatusId=str(doc["taskStatusId"]) if doc.get("taskStatusId") else None,
        taskPointId=str(doc["taskPointId"]) if doc.get("taskPointId") else None,
        dueDate=doc.get("dueDate"),
        startDate=doc.get("startDate"),
        done=bool(doc.get("done", False)),
        order=doc["order"],
        cover=doc.get("cover"),
        tagIds=[str(t) for t in doc.get("tagIds", [])],
        createdBy=str(doc["createdBy"]),
        updatedBy=str(doc["updatedBy"]) if doc.get("updatedBy") else None,
        createdAt=doc["createdAt"],
        updatedAt=doc.get("updatedAt"),
        doneAt=doc.get("doneAt"),
    )


def _to_checklist_response(doc: TaskChecklistDocument) -> ChecklistResponse:
    return ChecklistResponse(
        id=str(doc["_id"]),
        title=doc["title"],
        taskId=str(doc["taskId"]),
        done=bool(doc.get("done", False)),
        doneBy=str(doc["doneBy"]) if doc.get("doneBy") else None,
        createdBy=str(doc["createdBy"]),
        createdAt=doc["createdAt"],
        updatedAt=doc.get("updatedAt"),
        order=doc["order"],
    )


def _to_comment_response(doc: TaskCommentDocument) -> CommentResponse:
    return CommentResponse(
        id=str(doc["_id"]),
        content=doc["content"],
        taskId=str(doc["taskId"]),
        createdBy=str(doc["createdBy"]),
        updatedBy=str(doc["updatedBy"]) if doc.get("updatedBy") else None,
        createdAt=doc["createdAt"],
        updatedAt=doc.get("updatedAt"),
    )


def _to_activity_response(doc: TaskActivityDocument) -> ActivityResponse:
    return ActivityResponse(
        id=str(doc["_id"]),
        objectId=str(doc["objectId"]),
        type=doc["type"],
        data=doc["data"],
        createdBy=str(doc["createdBy"]),
        createdAt=doc["createdAt"],
        updatedAt=doc.get("updatedAt"),
    )