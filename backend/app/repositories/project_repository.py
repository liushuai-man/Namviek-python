from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Protocol, cast

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.asynchronous.database import AsyncDatabase

from app.db.mongodb import Document
from app.models.project import (
    ProjectDocument,
    ProjectStatusDocument,
    ProjectViewDocument,
)


class ProjectRepositoryProtocol(Protocol):
    async def create(
        self,
        *,
        name: str,
        desc: str,
        icon: str | None,
        color: str | None,
        organization_id: ObjectId,
        created_by: ObjectId,
    ) -> ProjectDocument: ...

    async def find_by_id(self, project_id: str) -> ProjectDocument | None: ...

    async def find_by_org_id(
        self, org_id: str, *, is_archived: bool = False
    ) -> list[ProjectDocument]: ...

    async def update(
        self, project_id: ObjectId, updates: dict[str, object]
    ) -> ProjectDocument | None: ...

    async def archive(
        self, project_id: ObjectId, archived: bool, archived_by: ObjectId
    ) -> ProjectDocument | None: ...

    # ── Status ──
    async def create_status(
        self, *, name: str, color: str | None, order: int, project_id: ObjectId
    ) -> ProjectStatusDocument: ...

    async def find_statuses_by_project(
        self, project_id: str
    ) -> list[ProjectStatusDocument]: ...

    async def update_status(
        self, status_id: ObjectId, updates: dict[str, object]
    ) -> ProjectStatusDocument | None: ...

    async def update_status_order(
        self, orders: list[tuple[ObjectId, int]]
    ) -> None: ...

    async def delete_status(self, status_id: ObjectId) -> bool: ...

    # ── View ──
    async def create_view(
        self,
        *,
        name: str,
        type_: str,
        icon: str | None,
        order: int,
        data: dict[str, object],
        project_id: ObjectId,
    ) -> ProjectViewDocument: ...

    async def find_views_by_project(
        self, project_id: str
    ) -> list[ProjectViewDocument]: ...

    async def find_view_by_id(self, view_id: str) -> ProjectViewDocument | None: ...

    async def update_view(
        self, view_id: ObjectId, updates: dict[str, object]
    ) -> ProjectViewDocument | None: ...

    async def delete_view(self, view_id: ObjectId) -> bool: ...


class MongoProjectRepository:
    def __init__(self, database: AsyncDatabase[Document]) -> None:
        self._database = database
        self._projects = database.projects
        self._statuses = database.project_statuses
        self._views = database.project_views
        self._points = database.project_points
        self._tags = database.project_tags
        self._members = database.project_members

    # ── Project CRUD ─────────────────────────────────────────────────

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
        now = datetime.now(UTC)
        document: Document = {
            "name": name,
            "desc": desc,
            "icon": icon,
            "color": color,
            "cover": None,
            "organizationId": organization_id,
            "createdBy": created_by,
            "createdAt": now,
            "updatedAt": None,
            "archivedAt": None,
            "archivedBy": None,
            "allMemberVisible": False,
        }
        result = await self._projects.insert_one(document)
        document["_id"] = result.inserted_id
        return _as_project_document(document)

    async def find_by_id(self, project_id: str) -> ProjectDocument | None:
        try:
            oid = ObjectId(project_id)
        except InvalidId:
            return None
        doc = await self._projects.find_one({"_id": oid})
        return _as_project_document(doc) if doc else None

    async def find_by_org_id(
        self, org_id: str, *, is_archived: bool = False
    ) -> list[ProjectDocument]:
        try:
            oid = ObjectId(org_id)
        except InvalidId:
            return []
        query: dict[str, object] = {"organizationId": oid}
        if is_archived:
            query["archivedAt"] = {"$ne": None}
        else:
            query["archivedAt"] = None
        cursor = self._projects.find(query).sort("createdAt", -1)
        return [_as_project_document(d) async for d in cursor]

    async def update(
        self, project_id: ObjectId, updates: dict[str, object]
    ) -> ProjectDocument | None:
        updates["updatedAt"] = datetime.now(UTC)
        doc = await self._projects.find_one_and_update(
            {"_id": project_id},
            {"$set": updates},
            return_document=True,
        )
        return _as_project_document(doc) if doc else None

    async def archive(
        self, project_id: ObjectId, archived: bool, archived_by: ObjectId
    ) -> ProjectDocument | None:
        now = datetime.now(UTC)
        updates: dict[str, object] = {
            "updatedAt": now,
            "archivedAt": now if archived else None,
            "archivedBy": archived_by if archived else None,
        }
        return await self.update(project_id, updates)

    # ── Status ───────────────────────────────────────────────────────

    async def create_status(
        self, *, name: str, color: str | None, order: int, project_id: ObjectId
    ) -> ProjectStatusDocument:
        now = datetime.now(UTC)
        document: Document = {
            "name": name,
            "color": color,
            "order": order,
            "projectId": project_id,
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._statuses.insert_one(document)
        document["_id"] = result.inserted_id
        return _as_status_document(document)

    async def find_statuses_by_project(
        self, project_id: str
    ) -> list[ProjectStatusDocument]:
        try:
            oid = ObjectId(project_id)
        except InvalidId:
            return []
        cursor = self._statuses.find({"projectId": oid}).sort("order", 1)
        return [_as_status_document(d) async for d in cursor]

    async def update_status(
        self, status_id: ObjectId, updates: dict[str, object]
    ) -> ProjectStatusDocument | None:
        updates["updatedAt"] = datetime.now(UTC)
        doc = await self._statuses.find_one_and_update(
            {"_id": status_id}, {"$set": updates}, return_document=True
        )
        return _as_status_document(doc) if doc else None

    async def update_status_order(
        self, orders: list[tuple[ObjectId, int]]
    ) -> None:
        for oid, order in orders:
            await self._statuses.update_one(
                {"_id": oid}, {"$set": {"order": order, "updatedAt": datetime.now(UTC)}}
            )

    async def delete_status(self, status_id: ObjectId) -> bool:
        result = await self._statuses.delete_one({"_id": status_id})
        return result.deleted_count > 0

    # ── View ─────────────────────────────────────────────────────────

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
        now = datetime.now(UTC)
        document: Document = {
            "name": name,
            "type": type_,
            "icon": icon,
            "order": order,
            "data": data,
            "projectId": project_id,
            "createdAt": now,
            "updatedAt": None,
            "pinned": False,
        }
        result = await self._views.insert_one(document)
        document["_id"] = result.inserted_id
        return _as_view_document(document)

    async def find_views_by_project(
        self, project_id: str
    ) -> list[ProjectViewDocument]:
        try:
            oid = ObjectId(project_id)
        except InvalidId:
            return []
        cursor = self._views.find({"projectId": oid}).sort("order", 1)
        return [_as_view_document(d) async for d in cursor]

    async def find_view_by_id(self, view_id: str) -> ProjectViewDocument | None:
        try:
            oid = ObjectId(view_id)
        except InvalidId:
            return None
        doc = await self._views.find_one({"_id": oid})
        return _as_view_document(doc) if doc else None

    async def update_view(
        self, view_id: ObjectId, updates: dict[str, object]
    ) -> ProjectViewDocument | None:
        updates["updatedAt"] = datetime.now(UTC)
        doc = await self._views.find_one_and_update(
            {"_id": view_id}, {"$set": updates}, return_document=True
        )
        return _as_view_document(doc) if doc else None

    async def delete_view(self, view_id: ObjectId) -> bool:
        result = await self._views.delete_one({"_id": view_id})
        return result.deleted_count > 0


# ── Helper cast functions ────────────────────────────────────────────


def _as_project_document(document: Mapping[str, object]) -> ProjectDocument:
    return cast(ProjectDocument, dict(document))


def _as_status_document(document: Mapping[str, object]) -> ProjectStatusDocument:
    return cast(ProjectStatusDocument, dict(document))


def _as_view_document(document: Mapping[str, object]) -> ProjectViewDocument:
    return cast(ProjectViewDocument, dict(document))