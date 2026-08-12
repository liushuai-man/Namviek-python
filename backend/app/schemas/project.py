from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, model_validator


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
    organizationId: str = Field(alias="orgId")
    views: list[str] = Field(default_factory=lambda: ["BOARD"])
    members: list[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def normalize_org_id(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "orgId" not in data and "organizationId" in data:
                data["orgId"] = data["organizationId"]
            elif "organizationId" not in data and "orgId" in data:
                data["organizationId"] = data["orgId"]
        return data

    model_config = {"populate_by_name": True}


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
    orgId: str = Field(alias="organizationId")
    createdBy: str
    createdAt: datetime
    updatedAt: datetime | None = None
    archivedAt: datetime | None = None
    archivedBy: str | None = None
    allMemberVisible: bool = False

    model_config = {"populate_by_name": True}


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
    type: str
    icon: str | None = None
    order: int = 0
    data: dict[str, object] = Field(default_factory=dict)
    config: dict[str, object] = Field(default_factory=dict)
    projectId: str

    @model_validator(mode="before")
    @classmethod
    def merge_data_config(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "config" in data and "data" not in data:
                data["data"] = data["config"]
        return data


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
    data: dict[str, object] = Field(default_factory=dict)
    config: dict[str, object] = Field(default_factory=dict)
    projectId: str
    createdAt: datetime
    updatedAt: datetime | None = None
    pinned: bool = False

    @model_validator(mode="before")
    @classmethod
    def ensure_config(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "config" not in data and "data" in data:
                data["config"] = data["data"]
        return data


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