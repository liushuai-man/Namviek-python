from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Protocol, cast

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.asynchronous.database import AsyncDatabase

from app.db.mongodb import Document
from app.models.task import (
    TaskActivityDocument,
    TaskChecklistDocument,
    TaskCommentDocument,
    TaskDocument,
)


class TaskRepositoryProtocol(Protocol):
    async def create(self, **kwargs: object) -> TaskDocument: ...
    async def find_by_id(self, task_id: str) -> TaskDocument | None: ...
    async def find_by_project(
        self, project_id: str
    ) -> list[TaskDocument]: ...
    async def update(
        self, task_id: ObjectId, updates: dict[str, object]
    ) -> TaskDocument | None: ...
    async def update_many(
        self, ids: list[ObjectId], updates: dict[str, object]
    ) -> int: ...
    async def delete(self, task_id: ObjectId) -> bool: ...
    async def delete_many(self, ids: list[ObjectId]) -> int: ...
    async def update_order(
        self, orders: list[tuple[ObjectId, int]]
    ) -> None: ...
    async def count_by_status(
        self, project_ids: list[str]
    ) -> list[dict[str, object]]: ...


class MongoTaskRepository:
    def __init__(self, database: AsyncDatabase[Document]) -> None:
        self._tasks = database.tasks
        self._checklists = database.task_checklists
        self._comments = database.task_comments
        self._activities = database.task_activities

    # ── Task CRUD ────────────────────────────────────────────────────

    async def create(self, **kwargs: object) -> TaskDocument:
        now = datetime.now(UTC)
        document: Document = {
            "title": kwargs.get("title", ""),
            "desc": kwargs.get("desc", ""),
            "projectId": kwargs["projectId"],
            "statusId": kwargs.get("statusId"),
            "priority": kwargs.get("priority"),
            "assigneeIds": kwargs.get("assigneeIds", []),
            "taskStatusId": kwargs.get("taskStatusId"),
            "taskPointId": kwargs.get("taskPointId"),
            "dueDate": kwargs.get("dueDate"),
            "startDate": kwargs.get("startDate"),
            "done": kwargs.get("done", False),
            "order": kwargs.get("order", 0),
            "cover": kwargs.get("cover"),
            "tagIds": kwargs.get("tagIds", []),
            "createdBy": kwargs["createdBy"],
            "updatedBy": None,
            "createdAt": now,
            "updatedAt": None,
            "doneAt": now if kwargs.get("done") else None,
        }
        result = await self._tasks.insert_one(document)
        document["_id"] = result.inserted_id
        return _as_task_document(document)

    async def find_by_id(self, task_id: str) -> TaskDocument | None:
        try:
            oid = ObjectId(task_id)
        except InvalidId:
            return None
        doc = await self._tasks.find_one({"_id": oid})
        return _as_task_document(doc) if doc else None

    async def find_by_project(self, project_id: str) -> list[TaskDocument]:
        try:
            oid = ObjectId(project_id)
        except InvalidId:
            return []
        cursor = self._tasks.find({"projectId": oid}).sort("order", 1)
        return [_as_task_document(d) async for d in cursor]

    async def find_by_query(
        self,
        *,
        project_ids: list[ObjectId] | None = None,
        status_ids: list[ObjectId] | None = None,
        assignee_ids: list[ObjectId] | None = None,
        priority: str | None = None,
        done: bool | None = None,
        title: str | None = None,
        take: int | None = None,
        skip: int | None = None,
        order_by: tuple[str, int] | None = None,
    ) -> list[TaskDocument]:
        query: dict[str, object] = {}
        if project_ids:
            if len(project_ids) == 1:
                query["projectId"] = project_ids[0]
            else:
                query["projectId"] = {"$in": project_ids}
        if status_ids:
            query["statusId"] = {"$in": status_ids}
        if assignee_ids:
            query["assigneeIds"] = {"$in": assignee_ids}
        if priority:
            query["priority"] = priority
        if done is not None:
            query["done"] = done
        if title:
            query["title"] = {"$regex": title, "$options": "i"}

        sort_field = order_by[0] if order_by else "order"
        sort_dir = order_by[1] if order_by else 1
        cursor = self._tasks.find(query).sort(sort_field, sort_dir)
        if skip:
            cursor = cursor.skip(skip)
        if take:
            cursor = cursor.limit(take)
        return [_as_task_document(d) async for d in cursor]

    async def update(
        self, task_id: ObjectId, updates: dict[str, object]
    ) -> TaskDocument | None:
        updates["updatedAt"] = datetime.now(UTC)
        if "done" in updates and updates["done"]:
            updates["doneAt"] = datetime.now(UTC)
        doc = await self._tasks.find_one_and_update(
            {"_id": task_id}, {"$set": updates}, return_document=True
        )
        return _as_task_document(doc) if doc else None

    async def update_many(
        self, ids: list[ObjectId], updates: dict[str, object]
    ) -> int:
        updates["updatedAt"] = datetime.now(UTC)
        result = await self._tasks.update_many(
            {"_id": {"$in": ids}}, {"$set": updates}
        )
        return result.modified_count

    async def delete(self, task_id: ObjectId) -> bool:
        result = await self._tasks.delete_one({"_id": task_id})
        return result.deleted_count > 0

    async def delete_many(self, ids: list[ObjectId]) -> int:
        result = await self._tasks.delete_many({"_id": {"$in": ids}})
        return result.deleted_count

    async def update_order(self, orders: list[tuple[ObjectId, int]]) -> None:
        for oid, order in orders:
            await self._tasks.update_one(
                {"_id": oid}, {"$set": {"order": order, "updatedAt": datetime.now(UTC)}}
            )

    async def count_by_status(
        self, project_ids: list[str]
    ) -> list[dict[str, object]]:
        oids = [ObjectId(pid) for pid in project_ids]
        pipeline: list[dict[str, object]] = [
            {"$match": {"projectId": {"$in": oids}}},
            {
                "$group": {
                    "_id": "$statusId",
                    "count": {"$sum": 1},
                }
            },
        ]
        return [doc async for doc in self._tasks.aggregate(pipeline)]

    # ── Checklist ────────────────────────────────────────────────────

    async def create_checklist(self, **kwargs: object) -> TaskChecklistDocument:
        now = datetime.now(UTC)
        document: Document = {
            "title": kwargs["title"],
            "taskId": kwargs["taskId"],
            "done": kwargs.get("done", False),
            "doneBy": kwargs.get("doneBy"),
            "createdBy": kwargs["createdBy"],
            "createdAt": now,
            "updatedAt": None,
            "order": kwargs.get("order", 0),
        }
        result = await self._checklists.insert_one(document)
        document["_id"] = result.inserted_id
        return _as_checklist_document(document)

    async def find_checklists_by_task(
        self, task_id: str
    ) -> list[TaskChecklistDocument]:
        try:
            oid = ObjectId(task_id)
        except InvalidId:
            return []
        cursor = self._checklists.find({"taskId": oid}).sort("order", 1)
        return [_as_checklist_document(d) async for d in cursor]

    async def update_checklist(
        self, checklist_id: ObjectId, updates: dict[str, object]
    ) -> TaskChecklistDocument | None:
        updates["updatedAt"] = datetime.now(UTC)
        doc = await self._checklists.find_one_and_update(
            {"_id": checklist_id}, {"$set": updates}, return_document=True
        )
        return _as_checklist_document(doc) if doc else None

    async def delete_checklist(self, checklist_id: ObjectId) -> bool:
        result = await self._checklists.delete_one({"_id": checklist_id})
        return result.deleted_count > 0

    # ── Comment ───────────────────────────────────────────────────────

    async def create_comment(self, **kwargs: object) -> TaskCommentDocument:
        now = datetime.now(UTC)
        document: Document = {
            "content": kwargs["content"],
            "taskId": kwargs["taskId"],
            "createdBy": kwargs["createdBy"],
            "updatedBy": None,
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._comments.insert_one(document)
        document["_id"] = result.inserted_id
        return _as_comment_document(document)

    async def find_comments_by_task(self, task_id: str) -> list[TaskCommentDocument]:
        try:
            oid = ObjectId(task_id)
        except InvalidId:
            return []
        cursor = self._comments.find({"taskId": oid}).sort("createdAt", -1)
        return [_as_comment_document(d) async for d in cursor]

    async def update_comment(
        self, comment_id: ObjectId, updates: dict[str, object]
    ) -> TaskCommentDocument | None:
        updates["updatedAt"] = datetime.now(UTC)
        doc = await self._comments.find_one_and_update(
            {"_id": comment_id}, {"$set": updates}, return_document=True
        )
        return _as_comment_document(doc) if doc else None

    async def delete_comment(self, comment_id: ObjectId) -> bool:
        result = await self._comments.delete_one({"_id": comment_id})
        return result.deleted_count > 0

    # ── Activity ──────────────────────────────────────────────────────

    async def create_activity(self, **kwargs: object) -> TaskActivityDocument:
        now = datetime.now(UTC)
        document: Document = {
            "objectId": kwargs["objectId"],
            "type": kwargs["type"],
            "data": kwargs.get("data", {}),
            "createdBy": kwargs["createdBy"],
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._activities.insert_one(document)
        document["_id"] = result.inserted_id
        return _as_activity_document(document)

    async def find_activities_by_object(
        self, object_id: str
    ) -> list[TaskActivityDocument]:
        try:
            oid = ObjectId(object_id)
        except InvalidId:
            return []
        cursor = self._activities.find({"objectId": oid}).sort("createdAt", -1)
        return [_as_activity_document(d) async for d in cursor]

    async def update_activity(
        self, activity_id: ObjectId, updates: dict[str, object]
    ) -> TaskActivityDocument | None:
        updates["updatedAt"] = datetime.now(UTC)
        doc = await self._activities.find_one_and_update(
            {"_id": activity_id}, {"$set": updates}, return_document=True
        )
        return _as_activity_document(doc) if doc else None

    async def delete_activity(self, activity_id: ObjectId) -> bool:
        result = await self._activities.delete_one({"_id": activity_id})
        return result.deleted_count > 0


# ── Helpers ────────────────────────────────────────────────────────────


def _as_task_document(document: Mapping[str, object]) -> TaskDocument:
    return cast(TaskDocument, dict(document))


def _as_checklist_document(document: Mapping[str, object]) -> TaskChecklistDocument:
    return cast(TaskChecklistDocument, dict(document))


def _as_comment_document(document: Mapping[str, object]) -> TaskCommentDocument:
    return cast(TaskCommentDocument, dict(document))


def _as_activity_document(document: Mapping[str, object]) -> TaskActivityDocument:
    return cast(TaskActivityDocument, dict(document))