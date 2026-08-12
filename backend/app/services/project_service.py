from bson import ObjectId

from app.core.errors import AppError
from app.models.project import ProjectDocument, ProjectViewDocument
from app.repositories.project_repository import ProjectRepositoryProtocol
from app.schemas.project import (
    ProjectCreateRequest,
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


class ProjectService:
    def __init__(self, repository: ProjectRepositoryProtocol) -> None:
        self._repo = repository

    # ── Project CRUD ─────────────────────────────────────────────────

    async def create_project(
        self, data: ProjectCreateRequest, user_id: str
    ) -> ProjectResponse:
        project = await self._repo.create(
            name=data.name,
            desc=data.desc,
            icon=data.icon,
            color=data.color,
            organization_id=ObjectId(data.organizationId),
            created_by=ObjectId(user_id),
        )
        # Create default statuses for the new project
        default_statuses = [
            ("Todo", "#a1a1aa", 0),
            ("In Progress", "#3b82f6", 1),
            ("Done", "#22c55e", 2),
        ]
        for name, color, order in default_statuses:
            await self._repo.create_status(
                name=name, color=color, order=order, project_id=project["_id"]
            )
        return _to_project_response(project)

    async def get_projects(
        self, org_id: str, *, is_archived: bool = False
    ) -> list[ProjectResponse]:
        projects = await self._repo.find_by_org_id(org_id, is_archived=is_archived)
        return [_to_project_response(p) for p in projects]

    async def update_project(
        self, data: ProjectUpdateRequest, _user_id: str
    ) -> ProjectResponse:
        project = await self._repo.find_by_id(data.id)
        if not project:
            raise AppError(404, "not_found", "Project not found")
        updates: dict[str, object] = {}
        if data.name is not None:
            updates["name"] = data.name
        if data.desc is not None:
            updates["desc"] = data.desc
        if data.icon is not None:
            updates["icon"] = data.icon
        if data.color is not None:
            updates["color"] = data.color
        if data.cover is not None:
            updates["cover"] = data.cover
        if data.allMemberVisible is not None:
            updates["allMemberVisible"] = data.allMemberVisible
        updated = await self._repo.update(ObjectId(data.id), updates)
        if not updated:
            raise AppError(404, "not_found", "Project not found")
        return _to_project_response(updated)

    async def archive_project(
        self, project_id: str, archived: bool, user_id: str
    ) -> ProjectResponse:
        project = await self._repo.archive(
            ObjectId(project_id), archived, ObjectId(user_id)
        )
        if not project:
            raise AppError(404, "not_found", "Project not found")
        return _to_project_response(project)

    # ── Status ───────────────────────────────────────────────────────

    async def create_status(
        self, data: ProjectStatusCreateRequest
    ) -> ProjectStatusResponse:
        status = await self._repo.create_status(
            name=data.name,
            color=data.color,
            order=data.order,
            project_id=ObjectId(data.projectId),
        )
        return _to_status_response(status)

    async def get_statuses(self, project_id: str) -> list[ProjectStatusResponse]:
        statuses = await self._repo.find_statuses_by_project(project_id)
        return [_to_status_response(s) for s in statuses]

    async def update_status(
        self, data: ProjectStatusUpdateRequest
    ) -> ProjectStatusResponse:
        updates: dict[str, object] = {}
        if data.name is not None:
            updates["name"] = data.name
        if data.color is not None:
            updates["color"] = data.color
        if data.order is not None:
            updates["order"] = data.order
        status = await self._repo.update_status(ObjectId(data.id), updates)
        if not status:
            raise AppError(404, "not_found", "Status not found")
        return _to_status_response(status)

    async def update_status_order(
        self, data: ProjectStatusOrderRequest
    ) -> None:
        orders: list[tuple[ObjectId, int]] = []
        for item in data.newOrders:
            try:
                oid = ObjectId(str(item["id"]))
                order = int(item["order"])
                orders.append((oid, order))
            except Exception:
                continue
        await self._repo.update_status_order(orders)

    async def delete_status(self, status_id: str) -> None:
        deleted = await self._repo.delete_status(ObjectId(status_id))
        if not deleted:
            raise AppError(404, "not_found", "Status not found")

    # ── View ─────────────────────────────────────────────────────────

    async def create_view(
        self, data: ProjectViewCreateRequest
    ) -> ProjectViewResponse:
        view = await self._repo.create_view(
            name=data.name,
            type_=data.type,
            icon=data.icon,
            order=data.order,
            data=data.data,
            project_id=ObjectId(data.projectId),
        )
        return _to_view_response(view)

    async def get_views(self, project_id: str) -> list[ProjectViewResponse]:
        views = await self._repo.find_views_by_project(project_id)
        return [_to_view_response(v) for v in views]

    async def get_view(self, view_id: str) -> ProjectViewResponse:
        view = await self._repo.find_view_by_id(view_id)
        if not view:
            raise AppError(404, "not_found", "View not found")
        return _to_view_response(view)

    async def update_view(
        self, data: ProjectViewUpdateRequest
    ) -> ProjectViewResponse:
        updates: dict[str, object] = {}
        if data.name is not None:
            updates["name"] = data.name
        if data.icon is not None:
            updates["icon"] = data.icon
        if data.order is not None:
            updates["order"] = data.order
        if data.data is not None:
            updates["data"] = data.data
        if data.pinned is not None:
            updates["pinned"] = data.pinned
        view = await self._repo.update_view(ObjectId(data.id), updates)
        if not view:
            raise AppError(404, "not_found", "View not found")
        return _to_view_response(view)

    async def delete_view(self, view_id: str) -> None:
        deleted = await self._repo.delete_view(ObjectId(view_id))
        if not deleted:
            raise AppError(404, "not_found", "View not found")


# ── Response helpers ─────────────────────────────────────────────────


def _to_project_response(doc: ProjectDocument) -> ProjectResponse:
    return ProjectResponse(
        id=str(doc["_id"]),
        name=doc["name"],
        desc=doc["desc"],
        icon=doc.get("icon"),
        color=doc.get("color"),
        cover=doc.get("cover"),
        organizationId=str(doc["organizationId"]),
        createdBy=str(doc["createdBy"]),
        createdAt=doc["createdAt"],
        updatedAt=doc.get("updatedAt"),
        archivedAt=doc.get("archivedAt"),
        archivedBy=str(doc["archivedBy"]) if doc.get("archivedBy") else None,
        allMemberVisible=bool(doc.get("allMemberVisible", False)),
    )


def _to_status_response(doc: object) -> ProjectStatusResponse:
    d = dict(doc)  # type: ignore[arg-type]
    return ProjectStatusResponse(
        id=str(d["_id"]),
        name=d["name"],
        color=d.get("color"),
        order=d["order"],
        projectId=str(d["projectId"]),
        createdAt=d["createdAt"],
        updatedAt=d.get("updatedAt"),
    )


def _to_view_response(doc: ProjectViewDocument) -> ProjectViewResponse:
    return ProjectViewResponse(
        id=str(doc["_id"]),
        name=doc["name"],
        type=doc["type"],
        icon=doc.get("icon"),
        order=doc["order"],
        data=doc["data"],
        projectId=str(doc["projectId"]),
        createdAt=doc["createdAt"],
        updatedAt=doc.get("updatedAt"),
        pinned=bool(doc.get("pinned", False)),
    )