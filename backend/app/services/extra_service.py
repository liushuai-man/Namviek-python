from collections.abc import Mapping
from datetime import UTC, datetime

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.asynchronous.database import AsyncDatabase

from app.core.errors import AppError
from app.db.mongodb import Document
from app.repositories.org_repository import MongoOrgRepository
from app.repositories.user_repository import MongoUserRepository
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


class ExtraService:
    def __init__(
        self,
        database: AsyncDatabase[Document],
        org_repo: MongoOrgRepository,
    ) -> None:
        self._db = database
        self._user_repo = MongoUserRepository(database)
        self._org_repo = org_repo
        self._automations = database.task_automations
        self._timers = database.timers
        self._schedulers = database.schedulers
        self._rooms = database.meeting_rooms
        self._files = database.file_storages
        self._points = database.project_points
        self._tags = database.project_tags
        self._apps = database.applications
        self._org_members = database.organization_members

    # ── Automation ────────────────────────────────────────────────────

    async def get_automations(self, project_id: str) -> list[AutomationResponse]:
        try:
            oid = ObjectId(project_id)
        except InvalidId:
            return []
        cursor = self._automations.find({"projectId": oid}).sort("createdAt", -1)
        return [_to_auto_resp(d) async for d in cursor]

    async def create_automation(
        self, data: AutomationCreateRequest, user_id: str
    ) -> AutomationResponse:
        now = datetime.now(UTC)
        doc: Document = {
            "projectId": ObjectId(data.projectId),
            "trigger": data.trigger,
            "action": data.action,
            "createdBy": ObjectId(user_id),
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._automations.insert_one(doc)
        doc["_id"] = result.inserted_id
        return _to_auto_resp(doc)

    async def update_automation(
        self, data: AutomationUpdateRequest
    ) -> AutomationResponse:
        updates: dict[str, object] = {"updatedAt": datetime.now(UTC)}
        if data.trigger is not None:
            updates["trigger"] = data.trigger
        if data.action is not None:
            updates["action"] = data.action
        doc = await self._automations.find_one_and_update(
            {"_id": ObjectId(data.id)}, {"$set": updates}, return_document=True
        )
        if not doc:
            raise AppError(404, "not_found", "Automation not found")
        return _to_auto_resp(doc)

    async def delete_automation(self, auto_id: str) -> None:
        result = await self._automations.delete_one({"_id": ObjectId(auto_id)})
        if not result.deleted_count:
            raise AppError(404, "not_found", "Automation not found")

    # ── Timer ─────────────────────────────────────────────────────────

    async def start_timer(
        self, data: TimerStartRequest, user_id: str
    ) -> TimerLogResponse:
        now = datetime.now(UTC)
        doc: Document = {
            "taskId": ObjectId(data.taskId),
            "createdBy": ObjectId(user_id),
            "startedAt": now,
            "stoppedAt": None,
            "duration": None,
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._timers.insert_one(doc)
        doc["_id"] = result.inserted_id
        return _to_timer_resp(doc)

    async def stop_timer(
        self, data: TimerStopRequest, user_id: str
    ) -> TimerLogResponse:
        now = datetime.now(UTC)
        query: dict[str, object] = {
            "createdBy": ObjectId(user_id), "stoppedAt": None
        }
        if data.timerId:
            query["_id"] = ObjectId(data.timerId)
        doc = await self._timers.find_one_and_update(
            query,
            {
                "$set": {
                    "stoppedAt": now,
                    "duration": None,  # computed on read
                    "updatedAt": now,
                }
            },
            sort=[("startedAt", -1)],
            return_document=True,
        )
        if not doc:
            raise AppError(404, "not_found", "No active timer found")
        # Compute duration
        started = doc["startedAt"]
        if isinstance(started, datetime):
            doc["duration"] = int((now - started).total_seconds())  # type: ignore[typeddict-item]
        return _to_timer_resp(doc)

    async def get_current_timer(self, user_id: str) -> TimerLogResponse | None:
        doc = await self._timers.find_one(
            {"createdBy": ObjectId(user_id), "stoppedAt": None}
        )
        return _to_timer_resp(doc) if doc else None

    async def get_timer_logs(
        self, task_id: str, page: int = 1, limit: int = 7
    ) -> list[TimerLogResponse]:
        try:
            oid = ObjectId(task_id)
        except InvalidId:
            return []
        skip = (page - 1) * limit
        cursor = (
            self._timers.find({"taskId": oid})
            .sort("createdAt", -1)
            .skip(skip)
            .limit(limit)
        )
        return [_to_timer_resp(d) async for d in cursor]

    # ── Scheduler ─────────────────────────────────────────────────────

    async def create_scheduler(
        self, data: SchedulerCreateRequest, user_id: str
    ) -> SchedulerResponse:
        now = datetime.now(UTC)
        doc: Document = {
            "organizationId": ObjectId(data.organizationId),
            "projectId": ObjectId(data.projectId),
            "trigger": data.trigger,
            "action": data.action,
            "createdBy": ObjectId(user_id),
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._schedulers.insert_one(doc)
        doc["_id"] = result.inserted_id
        return _to_sched_resp(doc)

    async def get_schedulers(self, project_id: str) -> list[SchedulerResponse]:
        try:
            oid = ObjectId(project_id)
        except InvalidId:
            return []
        cursor = self._schedulers.find({"projectId": oid}).sort("createdAt", -1)
        return [_to_sched_resp(d) async for d in cursor]

    async def delete_scheduler(self, sched_id: str) -> None:
        result = await self._schedulers.delete_one({"_id": ObjectId(sched_id)})
        if not result.deleted_count:
            raise AppError(404, "not_found", "Scheduler not found")

    # ── Meeting ───────────────────────────────────────────────────────

    async def get_rooms(self) -> list[dict[str, object]]:
        cursor = self._rooms.find().sort("createdAt", -1)
        return [
            {"id": str(d["_id"]), "name": str(d["name"])}
            async for d in cursor
        ]

    async def create_room(self, name: str, user_id: str) -> dict[str, object]:
        now = datetime.now(UTC)
        doc: Document = {
            "name": name,
            "createdBy": ObjectId(user_id),
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._rooms.insert_one(doc)
        doc["_id"] = result.inserted_id
        return {"id": str(doc["_id"]), "name": name}

    async def delete_room(self, name: str) -> None:
        await self._rooms.delete_one({"name": name})

    # ── Storage ───────────────────────────────────────────────────────

    async def create_presigned_url(
        self, data: StoragePresignedUrlRequest, user_id: str
    ) -> dict[str, object]:
        # Placeholder - actual presigned URL generation requires S3/MinIO config
        return {
            "presignedUrl": f"/uploads/{data.orgId}/{data.projectId}/{data.name}",
            "keyName": f"{data.orgId}/{data.projectId}/{data.name}",
        }

    async def get_files(self, ids: list[str]) -> list[StorageFileResponse]:
        oids = [ObjectId(i) for i in ids]
        cursor = self._files.find({"_id": {"$in": oids}})
        return [_to_file_resp(d) async for d in cursor]

    async def delete_file(self, file_id: str) -> None:
        result = await self._files.delete_one({"_id": ObjectId(file_id)})
        if not result.deleted_count:
            raise AppError(404, "not_found", "File not found")

    async def save_to_drive(
        self, data: StorageSaveToDriveRequest, user_id: str
    ) -> StorageFileResponse:
        now = datetime.now(UTC)
        doc: Document = {
            "orgId": ObjectId(data.orgId),
            "projectId": ObjectId(data.projectId),
            "name": data.name,
            "type": data.type,
            "keyName": data.keyName,
            "url": data.url,
            "createdBy": ObjectId(user_id),
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._files.insert_one(doc)
        doc["_id"] = result.inserted_id
        return _to_file_resp(doc)

    # ── Report ────────────────────────────────────────────────────────

    async def get_project_report(self, query: ReportQueryRequest) -> dict[str, object]:
        return {"duration": query.duration, "projectIds": query.projectIds, "data": []}

    async def get_member_report(
        self, query: MemberReportQueryRequest
    ) -> dict[str, object]:
        return {
            "duration": query.duration,
            "projectIds": query.projectIds,
            "memberId": query.memberId,
            "data": [],
        }

    # ── Profile ───────────────────────────────────────────────────────

    async def get_profile(self, user_id: str) -> ProfileResponse:
        user = await self._user_repo.find_by_id(user_id)
        if not user:
            raise AppError(404, "not_found", "User not found")
        return ProfileResponse(
            id=str(user["_id"]),
            email=user["email"],
            name=user["name"],
            photo=user.get("photo"),
            bio=user.get("settings", {}).get("bio"),  # type: ignore[arg-type]
            createdAt=user["created_at"],
            updatedAt=user.get("updated_at"),
        )

    async def update_profile(
        self, data: ProfileUpdateRequest, user_id: str
    ) -> ProfileResponse:
        updates: dict[str, object] = {}
        if data.name is not None:
            updates["name"] = data.name
        if data.photo is not None:
            updates["photo"] = data.photo
        if data.bio is not None:
            updates["settings.bio"] = data.bio
        user = await self._user_repo.update(ObjectId(user_id), updates)
        if not user:
            raise AppError(404, "not_found", "User not found")
        return ProfileResponse(
            id=str(user["_id"]),
            email=user["email"],
            name=user["name"],
            photo=user.get("photo"),
            bio=user.get("settings", {}).get("bio"),  # type: ignore[arg-type]
            createdAt=user["created_at"],
            updatedAt=user.get("updated_at"),
        )

    async def update_password(
        self, data: PasswordUpdateRequest, user_id: str
    ) -> None:
        from app.core.security import hash_password, verify_password

        user = await self._user_repo.find_by_id(user_id)
        if not user:
            raise AppError(404, "not_found", "User not found")
        if not verify_password(data.currentPassword, user["password_hash"]):
            raise AppError(400, "invalid_password", "Current password is incorrect")
        if data.newPassword != data.confirmPassword:
            raise AppError(400, "password_mismatch", "Passwords do not match")
        await self._user_repo.update(
            ObjectId(user_id), {"password_hash": hash_password(data.newPassword)}
        )

    # ── Org Member ────────────────────────────────────────────────────

    async def get_org_members(self, org_id: str) -> list[dict[str, object]]:
        try:
            oid = ObjectId(org_id)
        except InvalidId:
            return []
        cursor = self._org_members.find({"orgId": oid})
        return [
            {
                "id": str(d["_id"]),
                "uid": str(d.get("uid", "")),
                "orgId": str(d["orgId"]),
                "email": str(d.get("email", "")),
                "role": str(d.get("role", "member")),
            }
            async for d in cursor
        ]

    async def search_org_members(
        self, data: OrgMemberSearchRequest
    ) -> list[dict[str, object]]:
        try:
            oid = ObjectId(data.orgId)
        except InvalidId:
            return []
        cursor = self._org_members.find(
            {
                "orgId": oid,
                "$or": [
                    {"email": {"$regex": data.term, "$options": "i"}},
                    {"name": {"$regex": data.term, "$options": "i"}},
                ],
            }
        ).limit(20)
        return [
            {
                "id": str(d["_id"]),
                "uid": str(d.get("uid", "")),
                "email": str(d.get("email", "")),
            }
            async for d in cursor
        ]

    async def invite_org_member(
        self, data: OrgMemberInviteRequest, _user_id: str
    ) -> dict[str, object]:
        now = datetime.now(UTC)
        doc: Document = {
            "orgId": ObjectId(data.orgId),
            "email": data.email,
            "uid": None,
            "role": "member",
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._org_members.insert_one(doc)
        doc["_id"] = result.inserted_id
        return {"id": str(doc["_id"]), "email": data.email}

    async def remove_org_member(self, org_id: str, uid: str) -> None:
        result = await self._org_members.delete_one(
            {"orgId": ObjectId(org_id), "uid": ObjectId(uid)}
        )
        if not result.deleted_count:
            raise AppError(404, "not_found", "Member not found")

    # ── Apps ──────────────────────────────────────────────────────────

    async def get_apps(self, org_id: str) -> list[AppResponse]:
        try:
            oid = ObjectId(org_id)
        except InvalidId:
            return []
        cursor = self._apps.find({"orgId": oid}).sort("createdAt", -1)
        return [_to_app_resp(d) async for d in cursor]

    async def create_app(
        self, data: AppCreateRequest, user_id: str
    ) -> AppResponse:
        now = datetime.now(UTC)
        doc: Document = {
            "name": data.name,
            "desc": data.desc,
            "orgId": ObjectId(data.orgId),
            "createdBy": ObjectId(user_id),
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._apps.insert_one(doc)
        doc["_id"] = result.inserted_id
        return _to_app_resp(doc)

    async def update_app(self, data: AppUpdateRequest) -> AppResponse:
        updates: dict[str, object] = {"updatedAt": datetime.now(UTC)}
        if data.name is not None:
            updates["name"] = data.name
        if data.desc is not None:
            updates["desc"] = data.desc
        doc = await self._apps.find_one_and_update(
            {"_id": ObjectId(data.id)}, {"$set": updates}, return_document=True
        )
        if not doc:
            raise AppError(404, "not_found", "App not found")
        return _to_app_resp(doc)

    async def delete_app(self, app_id: str) -> None:
        result = await self._apps.delete_one({"_id": ObjectId(app_id)})
        if not result.deleted_count:
            raise AppError(404, "not_found", "App not found")

    # ── Project Point ─────────────────────────────────────────────────

    async def get_points(self, project_id: str) -> list[PointResponse]:
        try:
            oid = ObjectId(project_id)
        except InvalidId:
            return []
        cursor = self._points.find({"projectId": oid}).sort("order", 1)
        return [_to_point_resp(d) async for d in cursor]

    async def create_point(
        self, data: PointCreateRequest, user_id: str
    ) -> PointResponse:
        now = datetime.now(UTC)
        doc: Document = {
            "name": data.name,
            "value": data.value,
            "icon": data.icon,
            "order": data.order,
            "projectId": ObjectId(data.projectId),
            "createdAt": now,
            "updatedAt": None,
        }
        result = await self._points.insert_one(doc)
        doc["_id"] = result.inserted_id
        return _to_point_resp(doc)

    async def update_point(self, data: PointUpdateRequest) -> PointResponse:
        updates: dict[str, object] = {"updatedAt": datetime.now(UTC)}
        for f in ("name", "value", "icon", "order"):
            v = getattr(data, f, None)
            if v is not None:
                updates[f] = v
        doc = await self._points.find_one_and_update(
            {"_id": ObjectId(data.id)}, {"$set": updates}, return_document=True
        )
        if not doc:
            raise AppError(404, "not_found", "Point not found")
        return _to_point_resp(doc)

    async def delete_point(self, point_id: str) -> None:
        result = await self._points.delete_one({"_id": ObjectId(point_id)})
        if not result.deleted_count:
            raise AppError(404, "not_found", "Point not found")

    # ── Tag ───────────────────────────────────────────────────────────

    async def get_tags(self, project_id: str) -> list[dict[str, object]]:
        try:
            oid = ObjectId(project_id)
        except InvalidId:
            return []
        cursor = self._tags.find({"projectId": oid})
        return [
            {"id": str(d["_id"]), "name": str(d["name"]), "color": d.get("color")}
            async for d in cursor
        ]


# ── Response helpers ────────────────────────────────────────────────────


def _to_auto_resp(doc: Mapping[str, object]) -> AutomationResponse:
    return AutomationResponse(
        id=str(doc["_id"]),
        projectId=str(doc["projectId"]),
        trigger=dict(doc.get("trigger", {})),  # type: ignore[arg-type]
        action=dict(doc.get("action", {})),  # type: ignore[arg-type]
        createdBy=str(doc["createdBy"]),
        createdAt=doc["createdAt"],  # type: ignore[arg-type]
        updatedAt=doc.get("updatedAt"),  # type: ignore[arg-type]
    )


def _to_timer_resp(doc: Mapping[str, object]) -> TimerLogResponse:
    return TimerLogResponse(
        id=str(doc["_id"]),
        taskId=str(doc["taskId"]),
        createdBy=str(doc["createdBy"]),
        startedAt=doc["startedAt"],  # type: ignore[arg-type]
        stoppedAt=doc.get("stoppedAt"),  # type: ignore[arg-type]
        duration=doc.get("duration"),  # type: ignore[arg-type]
        createdAt=doc["createdAt"],  # type: ignore[arg-type]
        updatedAt=doc.get("updatedAt"),  # type: ignore[arg-type]
    )


def _to_sched_resp(doc: Mapping[str, object]) -> SchedulerResponse:
    return SchedulerResponse(
        id=str(doc["_id"]),
        organizationId=str(doc["organizationId"]),
        projectId=str(doc["projectId"]),
        trigger=dict(doc.get("trigger", {})),  # type: ignore[arg-type]
        action=dict(doc.get("action", {})),  # type: ignore[arg-type]
        createdBy=str(doc["createdBy"]),
        createdAt=doc["createdAt"],  # type: ignore[arg-type]
        updatedAt=doc.get("updatedAt"),  # type: ignore[arg-type]
    )


def _to_file_resp(doc: Mapping[str, object]) -> StorageFileResponse:
    return StorageFileResponse(
        id=str(doc["_id"]),
        orgId=str(doc["orgId"]),
        projectId=str(doc["projectId"]),
        name=str(doc["name"]),
        type=str(doc["type"]),
        keyName=str(doc["keyName"]),
        url=doc.get("url"),  # type: ignore[arg-type]
        createdBy=str(doc["createdBy"]),
        createdAt=doc["createdAt"],  # type: ignore[arg-type]
        updatedAt=doc.get("updatedAt"),  # type: ignore[arg-type]
    )


def _to_app_resp(doc: Mapping[str, object]) -> AppResponse:
    return AppResponse(
        id=str(doc["_id"]),
        name=str(doc["name"]),
        desc=str(doc.get("desc", "")),
        orgId=str(doc["orgId"]),
        createdBy=str(doc["createdBy"]),
        createdAt=doc["createdAt"],  # type: ignore[arg-type]
        updatedAt=doc.get("updatedAt"),  # type: ignore[arg-type]
    )


def _to_point_resp(doc: Mapping[str, object]) -> PointResponse:
    return PointResponse(
        id=str(doc["_id"]),
        name=str(doc["name"]),
        value=str(doc["value"]),
        icon=doc.get("icon"),  # type: ignore[arg-type]
        order=int(doc["order"]),
        projectId=str(doc["projectId"]),
        createdAt=doc["createdAt"],  # type: ignore[arg-type]
        updatedAt=doc.get("updatedAt"),  # type: ignore[arg-type]
    )