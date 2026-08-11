from collections.abc import Mapping
from datetime import UTC, datetime

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.asynchronous.database import AsyncDatabase

from app.db.mongodb import Document
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


class MongoOrgRepository:
    def __init__(self, database: AsyncDatabase[Document]) -> None:
        self._db = database
        self._orgs = database.organizations
        self._org_storages = database.organization_storages
        self._members = database.project_members
        self._favorites = database.favorites
        self._visions = database.visions
        self._dashboards = database.dashboards
        self._dboard_components = database.dashboard_components
        self._fields = database.custom_fields

    # ── Organization ──────────────────────────────────────────────────

    async def create_org(
        self, *, name: str, slug: str, description: str, created_by: ObjectId
    ) -> OrganizationDocument:
        now = datetime.now(UTC)
        doc: Document = {
            "name": name,
            "slug": slug,
            "description": description,
            "logo": None,
            "createdBy": created_by,
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._orgs.insert_one(doc)
        doc["_id"] = result.inserted_id
        return _doc(doc)

    async def find_org_by_id(self, org_id: str) -> OrganizationDocument | None:
        try:
            oid = ObjectId(org_id)
        except InvalidId:
            return None
        doc = await self._orgs.find_one({"_id": oid})
        return _doc(doc) if doc else None

    async def find_org_by_slug(self, slug: str) -> OrganizationDocument | None:
        doc = await self._orgs.find_one({"slug": slug})
        return _doc(doc) if doc else None

    async def find_orgs_by_user(self, user_id: ObjectId) -> list[OrganizationDocument]:
        cursor = self._orgs.find({"createdBy": user_id}).sort("createdAt", -1)
        return [_doc(d) async for d in cursor]

    async def update_org(
        self, org_id: ObjectId, updates: dict[str, object]
    ) -> OrganizationDocument | None:
        updates["updatedAt"] = datetime.now(UTC)
        doc = await self._orgs.find_one_and_update(
            {"_id": org_id}, {"$set": updates}, return_document=True
        )
        return _doc(doc) if doc else None

    # ── Org Storage ───────────────────────────────────────────────────

    async def upsert_org_storage(
        self, *, org_id: ObjectId, type_: str, config: dict[str, object]
    ) -> OrganizationStorageDocument:
        now = datetime.now(UTC)
        doc = await self._org_storages.find_one_and_update(
            {"orgId": org_id},
            {
                "$set": {
                    "type": type_,
                    "config": config,
                    "updatedAt": now,
                },
                "$setOnInsert": {"createdAt": now},
            },
            upsert=True,
            return_document=True,
        )
        return _doc(doc) if doc else _doc({})

    async def find_org_storage(
        self, org_id: str
    ) -> OrganizationStorageDocument | None:
        try:
            oid = ObjectId(org_id)
        except InvalidId:
            return None
        doc = await self._org_storages.find_one({"orgId": oid})
        return _doc(doc) if doc else None

    # ── Member ────────────────────────────────────────────────────────

    async def add_members(
        self, project_id: ObjectId, members: list[dict[str, object]]
    ) -> list[ProjectMemberDocument]:
        now = datetime.now(UTC)
        docs: list[Document] = []
        for m in members:
            doc: Document = {
                "projectId": project_id,
                "uid": ObjectId(str(m["uid"])),
                "role": m.get("role", "MEMBER"),
                "createdAt": now,
                "updatedAt": None,
            }
            docs.append(doc)
        if docs:
            result = await self._members.insert_many(docs)
            for i, doc in enumerate(docs):
                doc["_id"] = result.inserted_ids[i]
        return [_doc(d) for d in docs]

    async def find_members_by_project(
        self, project_id: str
    ) -> list[ProjectMemberDocument]:
        try:
            oid = ObjectId(project_id)
        except InvalidId:
            return []
        cursor = self._members.find({"projectId": oid})
        return [_doc(d) async for d in cursor]

    async def update_member_role(
        self, uid: ObjectId, project_id: ObjectId, role: str
    ) -> ProjectMemberDocument | None:
        updates = {"role": role, "updatedAt": datetime.now(UTC)}
        doc = await self._members.find_one_and_update(
            {"uid": uid, "projectId": project_id},
            {"$set": updates},
            return_document=True,
        )
        return _doc(doc) if doc else None

    async def remove_member(self, uid: ObjectId, project_id: ObjectId) -> bool:
        result = await self._members.delete_one(
            {"uid": uid, "projectId": project_id}
        )
        return result.deleted_count > 0

    # ── Favorite ──────────────────────────────────────────────────────

    async def create_favorite(
        self, *, org_id: ObjectId, uid: ObjectId, project_id: ObjectId,
        icon: str | None, name: str | None, type_: str,
    ) -> FavoriteDocument:
        now = datetime.now(UTC)
        doc: Document = {
            "orgId": org_id,
            "uid": uid,
            "projectId": project_id,
            "icon": icon,
            "name": name,
            "type": type_,
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._favorites.insert_one(doc)
        doc["_id"] = result.inserted_id
        return _doc(doc)

    async def find_favorites_by_org(self, org_id: str) -> list[FavoriteDocument]:
        try:
            oid = ObjectId(org_id)
        except InvalidId:
            return []
        cursor = self._favorites.find({"orgId": oid}).sort("createdAt", -1)
        return [_doc(d) async for d in cursor]

    async def delete_favorite(self, fav_id: ObjectId) -> bool:
        result = await self._favorites.delete_one({"_id": fav_id})
        return result.deleted_count > 0

    # ── Vision ────────────────────────────────────────────────────────

    async def create_vision(self, **kwargs: object) -> VisionDocument:
        now = datetime.now(UTC)
        doc: Document = {
            "projectId": kwargs["projectId"],
            "orgId": kwargs["orgId"],
            "title": kwargs["title"],
            "desc": kwargs.get("desc", ""),
            "progress": kwargs.get("progress", 0.0),
            "startDate": kwargs.get("startDate"),
            "endDate": kwargs.get("endDate"),
            "parentId": kwargs.get("parentId"),
            "createdBy": kwargs["createdBy"],
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._visions.insert_one(doc)
        doc["_id"] = result.inserted_id
        return _doc(doc)

    async def find_visions_by_project(self, project_id: str) -> list[VisionDocument]:
        try:
            oid = ObjectId(project_id)
        except InvalidId:
            return []
        cursor = self._visions.find({"projectId": oid}).sort("createdAt", -1)
        return [_doc(d) async for d in cursor]

    async def find_visions_by_org(self, org_id: str) -> list[VisionDocument]:
        try:
            oid = ObjectId(org_id)
        except InvalidId:
            return []
        cursor = self._visions.find({"orgId": oid}).sort("createdAt", -1)
        return [_doc(d) async for d in cursor]

    async def update_vision(
        self, vision_id: ObjectId, updates: dict[str, object]
    ) -> VisionDocument | None:
        updates["updatedAt"] = datetime.now(UTC)
        doc = await self._visions.find_one_and_update(
            {"_id": vision_id}, {"$set": updates}, return_document=True
        )
        return _doc(doc) if doc else None

    async def delete_vision(self, vision_id: ObjectId) -> bool:
        result = await self._visions.delete_one({"_id": vision_id})
        return result.deleted_count > 0

    # ── Dashboard ─────────────────────────────────────────────────────

    async def create_dashboard(
        self,
        *,
        project_id: ObjectId,
        title: str,
        is_default: bool,
        created_by: ObjectId,
    ) -> DashboardDocument:
        now = datetime.now(UTC)
        doc: Document = {
            "projectId": project_id,
            "title": title,
            "isDefault": is_default,
            "createdBy": created_by,
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._dashboards.insert_one(doc)
        doc["_id"] = result.inserted_id
        return _doc(doc)

    async def find_dashboards_by_project(
        self, project_id: str
    ) -> list[DashboardDocument]:
        try:
            oid = ObjectId(project_id)
        except InvalidId:
            return []
        cursor = self._dashboards.find({"projectId": oid}).sort("createdAt", -1)
        return [_doc(d) async for d in cursor]

    async def create_dboard_component(
        self, **kwargs: object
    ) -> DashboardComponentDocument:
        now = datetime.now(UTC)
        doc: Document = {
            "dboardId": kwargs["dboardId"],
            "type": kwargs["type"],
            "title": kwargs["title"],
            "icon": kwargs.get("icon"),
            "config": kwargs.get("config", {}),
            "x": kwargs.get("x", 0),
            "y": kwargs.get("y", 0),
            "width": kwargs.get("width", 4),
            "height": kwargs.get("height", 4),
            "createdBy": kwargs["createdBy"],
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._dboard_components.insert_one(doc)
        doc["_id"] = result.inserted_id
        return _doc(doc)

    async def find_dboard_components(
        self, dboard_id: str
    ) -> list[DashboardComponentDocument]:
        try:
            oid = ObjectId(dboard_id)
        except InvalidId:
            return []
        cursor = self._dboard_components.find({"dboardId": oid})
        return [_doc(d) async for d in cursor]

    async def delete_dboard_component(self, component_id: ObjectId) -> bool:
        result = await self._dboard_components.delete_one({"_id": component_id})
        return result.deleted_count > 0

    async def update_dboard_component(
        self, component_id: ObjectId, updates: dict[str, object]
    ) -> DashboardComponentDocument | None:
        updates["updatedAt"] = datetime.now(UTC)
        doc = await self._dboard_components.find_one_and_update(
            {"_id": component_id}, {"$set": updates}, return_document=True
        )
        return _doc(doc) if doc else None

    async def update_dboard_layout(
        self, updates: list[tuple[ObjectId, int, int, int, int]]
    ) -> None:
        for oid, x, y, w, h in updates:
            await self._dboard_components.update_one(
                {"_id": oid},
                {
                    "$set": {
                        "x": x, "y": y, "width": w, "height": h,
                        "updatedAt": datetime.now(UTC),
                    }
                },
            )

    # ── Custom Field ──────────────────────────────────────────────────

    async def create_field(self, **kwargs: object) -> CustomFieldDocument:
        now = datetime.now(UTC)
        doc: Document = {
            "name": kwargs["name"],
            "type": kwargs["type"],
            "icon": kwargs.get("icon"),
            "order": kwargs.get("order", 0),
            "visible": kwargs.get("visible", True),
            "projectId": kwargs["projectId"],
            "createdBy": kwargs["createdBy"],
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._fields.insert_one(doc)
        doc["_id"] = result.inserted_id
        return _doc(doc)

    async def find_fields_by_project(
        self, project_id: str
    ) -> list[CustomFieldDocument]:
        try:
            oid = ObjectId(project_id)
        except InvalidId:
            return []
        cursor = self._fields.find({"projectId": oid}).sort("order", 1)
        return [_doc(d) async for d in cursor]

    async def update_field(
        self, field_id: ObjectId, updates: dict[str, object]
    ) -> CustomFieldDocument | None:
        updates["updatedAt"] = datetime.now(UTC)
        doc = await self._fields.find_one_and_update(
            {"_id": field_id}, {"$set": updates}, return_document=True
        )
        return _doc(doc) if doc else None

    async def update_field_order(
        self, orders: list[tuple[ObjectId, int]]
    ) -> None:
        for oid, order in orders:
            await self._fields.update_one(
                {"_id": oid}, {"$set": {"order": order, "updatedAt": datetime.now(UTC)}}
            )

    async def delete_field(self, field_id: ObjectId) -> bool:
        result = await self._fields.delete_one({"_id": field_id})
        return result.deleted_count > 0


def _doc(doc: Mapping[str, object]) -> object:
    # Helper to cast Mapping to a mutable dict-like object.
    # Callers recast to the specific TypedDict via the return-type annotation.
    return dict(doc)