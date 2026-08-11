from datetime import datetime

from pydantic import BaseModel, Field

# ── Automation ────────────────────────────────────────────────────────────

class AutomationCreateRequest(BaseModel):
    projectId: str
    trigger: dict[str, object]
    action: dict[str, object]


class AutomationUpdateRequest(BaseModel):
    id: str
    trigger: dict[str, object] | None = None
    action: dict[str, object] | None = None


class AutomationResponse(BaseModel):
    id: str
    projectId: str
    trigger: dict[str, object]
    action: dict[str, object]
    createdBy: str
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Timer ─────────────────────────────────────────────────────────────────

class TimerStartRequest(BaseModel):
    taskId: str


class TimerStopRequest(BaseModel):
    timerId: str | None = None


class TimerLogResponse(BaseModel):
    id: str
    taskId: str
    createdBy: str
    startedAt: datetime
    stoppedAt: datetime | None = None
    duration: int | None = None
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Scheduler ─────────────────────────────────────────────────────────────

class SchedulerCreateRequest(BaseModel):
    organizationId: str
    projectId: str
    trigger: dict[str, object]
    action: dict[str, object]


class SchedulerResponse(BaseModel):
    id: str
    organizationId: str
    projectId: str
    trigger: dict[str, object]
    action: dict[str, object]
    createdBy: str
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Meeting ───────────────────────────────────────────────────────────────

class MeetingRoomCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class MeetingRoomResponse(BaseModel):
    id: str
    name: str
    createdBy: str
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Storage ───────────────────────────────────────────────────────────────

class StoragePresignedUrlRequest(BaseModel):
    orgId: str
    projectId: str
    name: str
    type: str


class StorageSaveToDriveRequest(BaseModel):
    orgId: str
    projectId: str
    name: str
    type: str
    keyName: str
    url: str | None = None


class StorageFileResponse(BaseModel):
    id: str
    orgId: str
    projectId: str
    name: str
    type: str
    keyName: str
    url: str | None = None
    createdBy: str
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Report ────────────────────────────────────────────────────────────────

class ReportQueryRequest(BaseModel):
    duration: str
    projectIds: list[str]


class MemberReportQueryRequest(BaseModel):
    duration: str
    projectIds: list[str]
    memberId: str


# ── Profile ───────────────────────────────────────────────────────────────

class ProfileUpdateRequest(BaseModel):
    name: str | None = None
    bio: str | None = None
    photo: str | None = None


class PasswordUpdateRequest(BaseModel):
    currentPassword: str
    newPassword: str
    confirmPassword: str


class ProfileResponse(BaseModel):
    id: str
    email: str
    name: str
    photo: str | None = None
    bio: str | None = None
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Org Member ────────────────────────────────────────────────────────────

class OrgMemberInviteRequest(BaseModel):
    orgId: str
    email: str


class OrgMemberSearchRequest(BaseModel):
    projectId: str
    orgId: str
    term: str


# ── Apps ──────────────────────────────────────────────────────────────────

class AppCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    desc: str = ""
    orgId: str


class AppUpdateRequest(BaseModel):
    id: str
    name: str | None = None
    desc: str | None = None


class AppResponse(BaseModel):
    id: str
    name: str
    desc: str = ""
    orgId: str
    createdBy: str
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Project Point ─────────────────────────────────────────────────────────

class PointCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    value: str
    icon: str | None = None
    order: int = 0
    projectId: str


class PointUpdateRequest(BaseModel):
    id: str
    name: str | None = None
    value: str | None = None
    icon: str | None = None
    order: int | None = None


class PointResponse(BaseModel):
    id: str
    name: str
    value: str
    icon: str | None = None
    order: int
    projectId: str
    createdAt: datetime
    updatedAt: datetime | None = None