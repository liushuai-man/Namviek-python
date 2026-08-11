from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class ProjectViewType(StrEnum):
    BOARD = "BOARD"
    LIST = "LIST"
    CALENDAR = "CALENDAR"
    GANTT = "GANTT"
    TEAM = "TEAM"
    TIMELINE = "TIMELINE"
    WORKLOAD = "WORKLOAD"
    ACTIVITY = "ACTIVITY"


class MemberRole(StrEnum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    GUEST = "GUEST"


# ── Project ──────────────────────────────────────────────────────────────

class ProjectCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    desc: str = ""
    icon: str | None = None
    color: str | None = None
    organizationId: str
    views: list[str] = Field(default_factory=lambda: ["BOARD"])
    members: list[str] = Field(default_factory=list)


class ProjectUpdateRequest(BaseModel):
    id: str
    name: str | None = None
    desc: str | None = None
    icon: str | None = None
    color: str | None = None
    cover: str | None = None
    allMemberVisible: bool | None = None


class ProjectResponse(BaseModel):
    id: str
    name: str
    desc: str
    icon: str | None = None
    color: str | None = None
    cover: str | None = None
    organizationId: str
    createdBy: str
    createdAt: datetime
    updatedAt: datetime | None = None
    archivedAt: datetime | None = None
    archivedBy: str | None = None
    allMemberVisible: bool = False


# ── Project Status ───────────────────────────────────────────────────────

class ProjectStatusCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    color: str | None = None
    order: int = 0
    projectId: str


class ProjectStatusUpdateRequest(BaseModel):
    id: str
    name: str | None = None
    color: str | None = None
    order: int | None = None


class ProjectStatusOrderRequest(BaseModel):
    newOrders: list[dict[str, object]]


class ProjectStatusResponse(BaseModel):
    id: str
    name: str
    color: str | None = None
    order: int
    projectId: str
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Project View ─────────────────────────────────────────────────────────

class ProjectViewCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    type: ProjectViewType
    icon: str | None = None
    order: int = 0
    data: dict[str, object] = Field(default_factory=dict)
    projectId: str


class ProjectViewUpdateRequest(BaseModel):
    id: str
    name: str | None = None
    icon: str | None = None
    order: int | None = None
    data: dict[str, object] | None = None
    pinned: bool | None = None


class ProjectViewResponse(BaseModel):
    id: str
    name: str
    type: str
    icon: str | None = None
    order: int
    data: dict[str, object]
    projectId: str
    createdAt: datetime
    updatedAt: datetime | None = None
    pinned: bool = False


# ── Project Point ────────────────────────────────────────────────────────

class ProjectPointCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    value: str = Field(min_length=1, max_length=10)
    icon: str | None = None
    order: int = 0
    projectId: str


class ProjectPointUpdateRequest(BaseModel):
    id: str
    name: str | None = None
    value: str | None = None
    icon: str | None = None
    order: int | None = None
    projectId: str | None = None


class ProjectPointResponse(BaseModel):
    id: str
    name: str
    value: str
    icon: str | None = None
    order: int
    projectId: str
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Project Tag ──────────────────────────────────────────────────────────

class ProjectTagResponse(BaseModel):
    id: str
    name: str
    color: str | None = None
    projectId: str
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Project Member ───────────────────────────────────────────────────────

class MemberAddRequest(BaseModel):
    projectId: str
    members: list[dict[str, object]]


class MemberRoleUpdateRequest(BaseModel):
    uid: str
    projectId: str
    role: MemberRole


class MemberResponse(BaseModel):
    id: str
    uid: str
    projectId: str
    role: str
    createdAt: datetime
    updatedAt: datetime | None = None