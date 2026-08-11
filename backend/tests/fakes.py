from datetime import UTC, datetime

from bson import ObjectId

from app.models.project import (
    ProjectDocument,
    ProjectStatusDocument,
    ProjectViewDocument,
)
from app.models.task import (
    TaskActivityDocument,
    TaskChecklistDocument,
    TaskCommentDocument,
    TaskDocument,
)
from app.models.user import UserDocument


class FakeUserRepository:
    def __init__(self) -> None:
        self.users: dict[str, UserDocument] = {}

    async def create(
        self, *, email: str, password_hash: str, name: str
    ) -> UserDocument:
        user: UserDocument = {
            "_id": ObjectId(),
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "status": "ACTIVE",
            "photo": None,
            "settings": {},
            "created_at": datetime.now(UTC),
            "updated_at": None,
        }
        self.users[email] = user
        return user

    async def find_by_email(self, email: str) -> UserDocument | None:
        return self.users.get(email)

    async def find_by_id(self, user_id: str) -> UserDocument | None:
        return next(
            (user for user in self.users.values() if str(user["_id"]) == user_id),
            None,
        )


class FakeProjectRepository:
    def __init__(self) -> None:
        self.projects: list[ProjectDocument] = []
        self.statuses: list[ProjectStatusDocument] = []
        self.views: list[ProjectViewDocument] = []

    async def create(
        self,
        *,
        name: str,
        desc: str,
        icon: str | None,
        color: str | None,
        organization_id: ObjectId,
        created_by: ObjectId,
    ) -> ProjectDocument:
        project: ProjectDocument = {
            "_id": ObjectId(),
            "name": name,
            "desc": desc,
            "icon": icon,
            "color": color,
            "cover": None,
            "organizationId": organization_id,
            "createdBy": created_by,
            "createdAt": datetime.now(UTC),
            "updatedAt": None,
            "archivedAt": None,
            "archivedBy": None,
            "allMemberVisible": False,
        }
        self.projects.append(project)
        return project

    async def find_by_id(self, project_id: str) -> ProjectDocument | None:
        return next(
            (p for p in self.projects if str(p["_id"]) == project_id), None
        )

    async def find_by_org_id(
        self, org_id: str, *, is_archived: bool = False
    ) -> list[ProjectDocument]:
        return [
            p
            for p in self.projects
            if str(p["organizationId"]) == org_id
            and (p.get("archivedAt") is not None) == is_archived
        ]

    async def update(
        self, project_id: ObjectId, updates: dict[str, object]
    ) -> ProjectDocument | None:
        for p in self.projects:
            if p["_id"] == project_id:
                for k, v in updates.items():
                    p[k] = v  # type: ignore[literal-required]
                p["updatedAt"] = datetime.now(UTC)  # type: ignore[typeddict-item]
                return p
        return None

    async def archive(
        self, project_id: ObjectId, archived: bool, archived_by: ObjectId
    ) -> ProjectDocument | None:
        now = datetime.now(UTC)
        return await self.update(
            project_id,
            {
                "archivedAt": now if archived else None,
                "archivedBy": archived_by if archived else None,
            },
        )

    async def create_status(
        self, *, name: str, color: str | None, order: int, project_id: ObjectId
    ) -> ProjectStatusDocument:
        status: ProjectStatusDocument = {
            "_id": ObjectId(),
            "name": name,
            "color": color,
            "order": order,
            "projectId": project_id,
            "createdAt": datetime.now(UTC),
            "updatedAt": None,
        }
        self.statuses.append(status)
        return status

    async def find_statuses_by_project(
        self, project_id: str
    ) -> list[ProjectStatusDocument]:
        return sorted(
            [s for s in self.statuses if str(s["projectId"]) == project_id],
            key=lambda s: s["order"],
        )

    async def update_status(
        self, status_id: ObjectId, updates: dict[str, object]
    ) -> ProjectStatusDocument | None:
        for s in self.statuses:
            if s["_id"] == status_id:
                for k, v in updates.items():
                    s[k] = v  # type: ignore[literal-required]
                s["updatedAt"] = datetime.now(UTC)  # type: ignore[typeddict-item]
                return s
        return None

    async def update_status_order(
        self, orders: list[tuple[ObjectId, int]]
    ) -> None:
        for oid, order in orders:
            for s in self.statuses:
                if s["_id"] == oid:
                    s["order"] = order  # type: ignore[typeddict-item]

    async def delete_status(self, status_id: ObjectId) -> bool:
        before = len(self.statuses)
        self.statuses = [s for s in self.statuses if s["_id"] != status_id]
        return len(self.statuses) < before

    async def create_view(
        self,
        *,
        name: str,
        type_: str,
        icon: str | None,
        order: int,
        data: dict[str, object],
        project_id: ObjectId,
    ) -> ProjectViewDocument:
        view: ProjectViewDocument = {
            "_id": ObjectId(),
            "name": name,
            "type": type_,
            "icon": icon,
            "order": order,
            "data": data,
            "projectId": project_id,
            "createdAt": datetime.now(UTC),
            "updatedAt": None,
            "pinned": False,
        }
        self.views.append(view)
        return view

    async def find_views_by_project(
        self, project_id: str
    ) -> list[ProjectViewDocument]:
        return sorted(
            [v for v in self.views if str(v["projectId"]) == project_id],
            key=lambda v: v["order"],
        )

    async def find_view_by_id(self, view_id: str) -> ProjectViewDocument | None:
        return next((v for v in self.views if str(v["_id"]) == view_id), None)

    async def update_view(
        self, view_id: ObjectId, updates: dict[str, object]
    ) -> ProjectViewDocument | None:
        for v in self.views:
            if v["_id"] == view_id:
                for k, val in updates.items():
                    v[k] = val  # type: ignore[literal-required]
                v["updatedAt"] = datetime.now(UTC)  # type: ignore[typeddict-item]
                return v
        return None

    async def delete_view(self, view_id: ObjectId) -> bool:
        before = len(self.views)
        self.views = [v for v in self.views if v["_id"] != view_id]
        return len(self.views) < before


class FakeTaskRepository:
    def __init__(self) -> None:
        self.tasks: list[TaskDocument] = []
        self.checklists: list[TaskChecklistDocument] = []
        self.comments: list[TaskCommentDocument] = []
        self.activities: list[TaskActivityDocument] = []

    async def create(self, **kwargs: object) -> TaskDocument:
        now = datetime.now(UTC)
        task: TaskDocument = {
            "_id": ObjectId(),
            "title": str(kwargs.get("title", "")),
            "desc": str(kwargs.get("desc", "")),
            "projectId": kwargs["projectId"],
            "statusId": kwargs.get("statusId"),
            "priority": kwargs.get("priority"),
            "assigneeIds": kwargs.get("assigneeIds", []),
            "taskStatusId": kwargs.get("taskStatusId"),
            "taskPointId": kwargs.get("taskPointId"),
            "dueDate": kwargs.get("dueDate"),
            "startDate": kwargs.get("startDate"),
            "done": bool(kwargs.get("done", False)),
            "order": int(kwargs.get("order", 0)),
            "cover": kwargs.get("cover"),
            "tagIds": kwargs.get("tagIds", []),
            "createdBy": kwargs["createdBy"],
            "updatedBy": None,
            "createdAt": now,
            "updatedAt": None,
            "doneAt": now if kwargs.get("done") else None,
        }
        self.tasks.append(task)
        return task

    async def find_by_id(self, task_id: str) -> TaskDocument | None:
        return next((t for t in self.tasks if str(t["_id"]) == task_id), None)

    async def find_by_project(self, project_id: str) -> list[TaskDocument]:
        return sorted(
            [t for t in self.tasks if str(t["projectId"]) == project_id],
            key=lambda t: t["order"],
        )

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
        result = list(self.tasks)
        if project_ids:
            result = [t for t in result if t["projectId"] in project_ids]
        if status_ids:
            result = [t for t in result if t.get("statusId") in status_ids]
        if done is not None:
            result = [t for t in result if t.get("done") == done]
        if priority:
            result = [t for t in result if t.get("priority") == priority]
        if title:
            result = [t for t in result if title.lower() in str(t["title"]).lower()]
        if order_by:
            result.sort(key=lambda t: t.get(order_by[0], 0), reverse=order_by[1] == -1)  # type: ignore[arg-type]
        if skip:
            result = result[skip:]
        if take:
            result = result[:take]
        return result

    async def update(
        self, task_id: ObjectId, updates: dict[str, object]
    ) -> TaskDocument | None:
        for t in self.tasks:
            if t["_id"] == task_id:
                for k, v in updates.items():
                    t[k] = v  # type: ignore[literal-required]
                t["updatedAt"] = datetime.now(UTC)  # type: ignore[typeddict-item]
                if updates.get("done"):
                    t["doneAt"] = datetime.now(UTC)  # type: ignore[typeddict-item]
                return t
        return None

    async def update_many(
        self, ids: list[ObjectId], updates: dict[str, object]
    ) -> int:
        count = 0
        for t in self.tasks:
            if t["_id"] in ids:
                for k, v in updates.items():
                    t[k] = v  # type: ignore[literal-required]
                t["updatedAt"] = datetime.now(UTC)  # type: ignore[typeddict-item]
                count += 1
        return count

    async def delete(self, task_id: ObjectId) -> bool:
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["_id"] != task_id]
        return len(self.tasks) < before

    async def delete_many(self, ids: list[ObjectId]) -> int:
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["_id"] not in ids]
        return before - len(self.tasks)

    async def update_order(self, orders: list[tuple[ObjectId, int]]) -> None:
        for oid, order in orders:
            for t in self.tasks:
                if t["_id"] == oid:
                    t["order"] = order  # type: ignore[typeddict-item]

    async def count_by_status(
        self, project_ids: list[str]
    ) -> list[dict[str, object]]:
        return []

    async def create_checklist(self, **kwargs: object) -> TaskChecklistDocument:
        now = datetime.now(UTC)
        item: TaskChecklistDocument = {
            "_id": ObjectId(),
            "title": str(kwargs["title"]),
            "taskId": kwargs["taskId"],
            "done": bool(kwargs.get("done", False)),
            "doneBy": kwargs.get("doneBy"),
            "createdBy": kwargs["createdBy"],
            "createdAt": now,
            "updatedAt": None,
            "order": int(kwargs.get("order", 0)),
        }
        self.checklists.append(item)
        return item

    async def find_checklists_by_task(
        self, task_id: str
    ) -> list[TaskChecklistDocument]:
        return sorted(
            [c for c in self.checklists if str(c["taskId"]) == task_id],
            key=lambda c: c["order"],
        )

    async def update_checklist(
        self, checklist_id: ObjectId, updates: dict[str, object]
    ) -> "TaskChecklistDocument | None":
        for c in self.checklists:
            if c["_id"] == checklist_id:
                for k, v in updates.items():
                    c[k] = v  # type: ignore[literal-required]
                c["updatedAt"] = datetime.now(UTC)  # type: ignore[typeddict-item]
                return c
        return None

    async def delete_checklist(self, checklist_id: ObjectId) -> bool:
        before = len(self.checklists)
        self.checklists = [c for c in self.checklists if c["_id"] != checklist_id]
        return len(self.checklists) < before

    async def create_comment(self, **kwargs: object) -> TaskCommentDocument:
        now = datetime.now(UTC)
        comment: TaskCommentDocument = {
            "_id": ObjectId(),
            "content": str(kwargs["content"]),
            "taskId": kwargs["taskId"],
            "createdBy": kwargs["createdBy"],
            "updatedBy": None,
            "createdAt": now,
            "updatedAt": None,
        }
        self.comments.append(comment)
        return comment

    async def find_comments_by_task(
        self, task_id: str
    ) -> list[TaskCommentDocument]:
        return sorted(
            [c for c in self.comments if str(c["taskId"]) == task_id],
            key=lambda c: c["createdAt"],
            reverse=True,
        )

    async def update_comment(
        self, comment_id: ObjectId, updates: dict[str, object]
    ) -> "TaskCommentDocument | None":
        for c in self.comments:
            if c["_id"] == comment_id:
                for k, v in updates.items():
                    c[k] = v  # type: ignore[literal-required]
                c["updatedAt"] = datetime.now(UTC)  # type: ignore[typeddict-item]
                return c
        return None

    async def delete_comment(self, comment_id: ObjectId) -> bool:
        before = len(self.comments)
        self.comments = [c for c in self.comments if c["_id"] != comment_id]
        return len(self.comments) < before

    async def create_activity(self, **kwargs: object) -> TaskActivityDocument:
        now = datetime.now(UTC)
        activity: TaskActivityDocument = {
            "_id": ObjectId(),
            "objectId": kwargs["objectId"],
            "type": str(kwargs["type"]),
            "data": kwargs.get("data", {}),
            "createdBy": kwargs["createdBy"],
            "createdAt": now,
            "updatedAt": None,
        }
        self.activities.append(activity)
        return activity

    async def find_activities_by_object(
        self, object_id: str
    ) -> list[TaskActivityDocument]:
        return sorted(
            [a for a in self.activities if str(a["objectId"]) == object_id],
            key=lambda a: a["createdAt"],
            reverse=True,
        )

    async def update_activity(
        self, activity_id: ObjectId, updates: dict[str, object]
    ) -> "TaskActivityDocument | None":
        for a in self.activities:
            if a["_id"] == activity_id:
                for k, v in updates.items():
                    a[k] = v  # type: ignore[literal-required]
                a["updatedAt"] = datetime.now(UTC)  # type: ignore[typeddict-item]
                return a
        return None

    async def delete_activity(self, activity_id: ObjectId) -> bool:
        before = len(self.activities)
        self.activities = [a for a in self.activities if a["_id"] != activity_id]
        return len(self.activities) < before

