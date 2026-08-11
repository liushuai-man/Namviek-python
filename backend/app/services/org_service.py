from bson import ObjectId

from app.core.errors import AppError
from app.models.org import (
    CustomFieldDocument,
    DashboardComponentDocument,
    DashboardDocument,
    FavoriteDocument,
    OrganizationDocument,
    OrganizationStorageDocument,
    VisionDocument,
)
from app.models.project import ProjectMemberDocument
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


class OrgService:
    def __init__(self, repo: MongoOrgRepository) -> None:
        self._repo = repo

    # ── Organization ──────────────────────────────────────────────────

    async def create_org(self, data: OrgCreateRequest, user_id: str) -> OrgResponse:
        org = await self._repo.create_org(
            name=data.name,
            slug=data.slug,
            description=data.description,
            created_by=ObjectId(user_id),
        )
        return _to_org_response(org)

    async def get_orgs(self, user_id: str) -> list[OrgResponse]:
        orgs = await self._repo.find_orgs_by_user(ObjectId(user_id))
        return [_to_org_response(o) for o in orgs]

    async def get_org_by_id(self, org_id: str) -> OrgResponse:
        org = await self._repo.find_org_by_id(org_id)
        if not org:
            raise AppError(404, "not_found", "Organization not found")
        return _to_org_response(org)

    async def get_org_by_slug(self, slug: str) -> OrgResponse:
        org = await self._repo.find_org_by_slug(slug)
        if not org:
            raise AppError(404, "not_found", "Organization not found")
        return _to_org_response(org)

    async def update_org(
        self, data: OrgUpdateRequest, _user_id: str
    ) -> OrgResponse:
        updates: dict[str, object] = {}
        if data.name is not None:
            updates["name"] = data.name
        if data.description is not None:
            updates["description"] = data.description
        if data.logo is not None:
            updates["logo"] = data.logo
        org = await self._repo.update_org(ObjectId(data.id), updates)
        if not org:
            raise AppError(404, "not_found", "Organization not found")
        return _to_org_response(org)

    # ── Org Storage ───────────────────────────────────────────────────

    async def update_org_storage(
        self, data: OrgStorageUpdateRequest
    ) -> OrgStorageResponse:
        storage = await self._repo.upsert_org_storage(
            org_id=ObjectId(data.orgId),
            type_=data.type,
            config=data.config,
        )
        return _to_storage_response(storage)

    async def get_org_storage(self, org_id: str) -> OrgStorageResponse | None:
        storage = await self._repo.find_org_storage(org_id)
        return _to_storage_response(storage) if storage else None

    # ── Member ────────────────────────────────────────────────────────

    async def get_members(self, project_id: str) -> list[dict[str, object]]:
        members = await self._repo.find_members_by_project(project_id)
        return [_to_member_dict(m) for m in members]

    async def add_members(
        self, project_id: str, members: list[dict[str, object]]
    ) -> list[dict[str, object]]:
        result = await self._repo.add_members(ObjectId(project_id), members)
        return [_to_member_dict(m) for m in result]

    async def update_member_role(
        self, uid: str, project_id: str, role: str
    ) -> dict[str, object]:
        member = await self._repo.update_member_role(
            ObjectId(uid), ObjectId(project_id), role
        )
        if not member:
            raise AppError(404, "not_found", "Member not found")
        return _to_member_dict(member)

    async def remove_member(self, uid: str, project_id: str) -> None:
        deleted = await self._repo.remove_member(
            ObjectId(uid), ObjectId(project_id)
        )
        if not deleted:
            raise AppError(404, "not_found", "Member not found")

    # ── Favorite ──────────────────────────────────────────────────────

    async def create_favorite(
        self, data: FavoriteCreateRequest, user_id: str
    ) -> FavoriteResponse:
        fav = await self._repo.create_favorite(
            org_id=ObjectId(data.orgId),
            uid=ObjectId(user_id),
            project_id=ObjectId(data.projectId),
            icon=data.icon,
            name=data.name,
            type_=data.type,
        )
        return _to_fav_response(fav)

    async def get_favorites(self, org_id: str) -> list[FavoriteResponse]:
        favs = await self._repo.find_favorites_by_org(org_id)
        return [_to_fav_response(f) for f in favs]

    async def delete_favorite(self, fav_id: str) -> None:
        deleted = await self._repo.delete_favorite(ObjectId(fav_id))
        if not deleted:
            raise AppError(404, "not_found", "Favorite not found")

    # ── Vision ────────────────────────────────────────────────────────

    async def create_vision(
        self, data: VisionCreateRequest, user_id: str
    ) -> VisionResponse:
        vision = await self._repo.create_vision(
            projectId=ObjectId(data.projectId),
            orgId=ObjectId(data.orgId),
            title=data.title,
            desc=data.desc,
            progress=data.progress,
            startDate=data.startDate,
            endDate=data.endDate,
            parentId=ObjectId(data.parentId) if data.parentId else None,
            createdBy=ObjectId(user_id),
        )
        return _to_vision_response(vision)

    async def get_visions_by_project(
        self, project_id: str
    ) -> list[VisionResponse]:
        visions = await self._repo.find_visions_by_project(project_id)
        return [_to_vision_response(v) for v in visions]

    async def get_visions_by_org(self, org_id: str) -> list[VisionResponse]:
        visions = await self._repo.find_visions_by_org(org_id)
        return [_to_vision_response(v) for v in visions]

    async def update_vision(
        self, data: VisionUpdateRequest
    ) -> VisionResponse:
        updates: dict[str, object] = {}
        for field in ("title", "desc", "progress", "startDate", "endDate"):
            value = getattr(data, field, None)
            if value is not None:
                updates[field] = value
        if data.parentId is not None:
            updates["parentId"] = ObjectId(data.parentId) if data.parentId else None
        vision = await self._repo.update_vision(ObjectId(data.id), updates)
        if not vision:
            raise AppError(404, "not_found", "Vision not found")
        return _to_vision_response(vision)

    async def delete_vision(self, vision_id: str) -> None:
        deleted = await self._repo.delete_vision(ObjectId(vision_id))
        if not deleted:
            raise AppError(404, "not_found", "Vision not found")

    # ── Dashboard ─────────────────────────────────────────────────────

    async def create_dashboard(
        self, data: DashboardCreateRequest, user_id: str
    ) -> DashboardResponse:
        dboard = await self._repo.create_dashboard(
            project_id=ObjectId(data.projectId),
            title=data.title,
            is_default=data.isDefault,
            created_by=ObjectId(user_id),
        )
        return _to_dboard_response(dboard)

    async def get_dashboards(self, project_id: str) -> list[DashboardResponse]:
        dboards = await self._repo.find_dashboards_by_project(project_id)
        return [_to_dboard_response(d) for d in dboards]

    async def create_dboard_component(
        self, data: DashboardComponentCreateRequest, user_id: str
    ) -> DashboardComponentResponse:
        comp = await self._repo.create_dboard_component(
            dboardId=ObjectId(data.dboardId),
            type=data.type,
            title=data.title,
            icon=data.icon,
            config=data.config,
            x=data.x,
            y=data.y,
            width=data.width,
            height=data.height,
            createdBy=ObjectId(user_id),
        )
        return _to_dboard_comp_response(comp)

    async def get_dboard_components(
        self, dboard_id: str
    ) -> list[DashboardComponentResponse]:
        comps = await self._repo.find_dboard_components(dboard_id)
        return [_to_dboard_comp_response(c) for c in comps]

    async def delete_dboard_component(self, component_id: str) -> None:
        deleted = await self._repo.delete_dboard_component(
            ObjectId(component_id)
        )
        if not deleted:
            raise AppError(404, "not_found", "Component not found")

    async def update_dboard_layout(
        self, data: DashboardLayoutUpdateRequest
    ) -> None:
        updates = [
            (ObjectId(c.id), c.x, c.y, c.width, c.height)
            for c in data.components
        ]
        await self._repo.update_dboard_layout(updates)

    # ── Custom Field ──────────────────────────────────────────────────

    async def create_field(
        self, data: FieldCreateRequest, user_id: str
    ) -> FieldResponse:
        field = await self._repo.create_field(
            name=data.name,
            type=data.type,
            icon=data.icon,
            order=data.order,
            visible=data.visible,
            projectId=ObjectId(data.projectId),
            createdBy=ObjectId(user_id),
        )
        return _to_field_response(field)

    async def get_fields(self, project_id: str) -> list[FieldResponse]:
        fields = await self._repo.find_fields_by_project(project_id)
        return [_to_field_response(f) for f in fields]

    async def update_field(self, data: FieldUpdateRequest) -> FieldResponse:
        updates: dict[str, object] = {}
        for field in ("name", "icon", "order", "visible"):
            value = getattr(data, field, None)
            if value is not None:
                updates[field] = value
        field = await self._repo.update_field(ObjectId(data.id), updates)
        if not field:
            raise AppError(404, "not_found", "Field not found")
        return _to_field_response(field)

    async def sort_fields(self, data: FieldSortableRequest) -> None:
        orders: list[tuple[ObjectId, int]] = []
        for item in data.items:
            orders.append((ObjectId(str(item["id"])), int(item["order"])))
        await self._repo.update_field_order(orders)

    async def delete_field(self, field_id: str) -> None:
        deleted = await self._repo.delete_field(ObjectId(field_id))
        if not deleted:
            raise AppError(404, "not_found", "Field not found")


# ── Response helpers ────────────────────────────────────────────────────


def _to_org_response(doc: OrganizationDocument) -> OrgResponse:
    return OrgResponse(
        id=str(doc["_id"]),
        name=doc["name"],
        slug=doc["slug"],
        description=doc.get("description", ""),
        logo=doc.get("logo"),
        createdBy=str(doc["createdBy"]),
        createdAt=doc["createdAt"],
        updatedAt=doc.get("updatedAt"),
    )


def _to_storage_response(doc: OrganizationStorageDocument) -> OrgStorageResponse:
    return OrgStorageResponse(
        id=str(doc["_id"]),
        orgId=str(doc["orgId"]),
        type=doc["type"],
        config=doc["config"],
        createdAt=doc["createdAt"],
        updatedAt=doc.get("updatedAt"),
    )


def _to_member_dict(doc: ProjectMemberDocument) -> dict[str, object]:
    return {
        "id": str(doc["_id"]),
        "uid": str(doc["uid"]),
        "projectId": str(doc["projectId"]),
        "role": doc["role"],
        "createdAt": doc["createdAt"].isoformat() if doc.get("createdAt") else None,
        "updatedAt": doc.get("updatedAt"),
    }


def _to_fav_response(doc: FavoriteDocument) -> FavoriteResponse:
    return FavoriteResponse(
        id=str(doc["_id"]),
        orgId=str(doc["orgId"]),
        uid=str(doc["uid"]),
        projectId=str(doc["projectId"]),
        icon=doc.get("icon"),
        name=doc.get("name"),
        type=doc["type"],
        createdAt=doc["createdAt"],
        updatedAt=doc.get("updatedAt"),
    )


def _to_vision_response(doc: VisionDocument) -> VisionResponse:
    return VisionResponse(
        id=str(doc["_id"]),
        projectId=str(doc["projectId"]),
        orgId=str(doc["orgId"]),
        title=doc["title"],
        desc=doc.get("desc", ""),
        progress=float(doc.get("progress", 0.0)),
        startDate=doc.get("startDate"),
        endDate=doc.get("endDate"),
        parentId=str(doc["parentId"]) if doc.get("parentId") else None,
        createdBy=str(doc["createdBy"]),
        createdAt=doc["createdAt"],
        updatedAt=doc.get("updatedAt"),
    )


def _to_dboard_response(doc: DashboardDocument) -> DashboardResponse:
    return DashboardResponse(
        id=str(doc["_id"]),
        projectId=str(doc["projectId"]),
        title=doc["title"],
        isDefault=bool(doc.get("isDefault", False)),
        createdBy=str(doc["createdBy"]),
        createdAt=doc["createdAt"],
        updatedAt=doc.get("updatedAt"),
    )


def _to_dboard_comp_response(
    doc: DashboardComponentDocument,
) -> DashboardComponentResponse:
    return DashboardComponentResponse(
        id=str(doc["_id"]),
        dboardId=str(doc["dboardId"]),
        type=doc["type"],
        title=doc["title"],
        icon=doc.get("icon"),
        config=doc["config"],
        x=doc["x"],
        y=doc["y"],
        width=doc["width"],
        height=doc["height"],
        createdBy=str(doc["createdBy"]),
        createdAt=doc["createdAt"],
        updatedAt=doc.get("updatedAt"),
    )


def _to_field_response(doc: CustomFieldDocument) -> FieldResponse:
    return FieldResponse(
        id=str(doc["_id"]),
        name=doc["name"],
        type=doc["type"],
        icon=doc.get("icon"),
        order=doc["order"],
        visible=bool(doc.get("visible", True)),
        projectId=str(doc["projectId"]),
        createdBy=str(doc["createdBy"]),
        createdAt=doc["createdAt"],
        updatedAt=doc.get("updatedAt"),
    )