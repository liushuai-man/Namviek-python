from datetime import datetime

from pydantic import BaseModel, Field

# ── Organization ──────────────────────────────────────────────────────────

class OrgCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=1, max_length=50)
    description: str = ""


class OrgUpdateRequest(BaseModel):
    id: str
    name: str | None = None
    description: str | None = None
    logo: str | None = None


class OrgStorageUpdateRequest(BaseModel):
    orgId: str
    type: str
    config: dict[str, object]


class OrgResponse(BaseModel):
    id: str
    name: str
    slug: str
    description: str = ""
    logo: str | None = None
    createdBy: str
    createdAt: datetime
    updatedAt: datetime | None = None


class OrgStorageResponse(BaseModel):
    id: str
    orgId: str
    type: str
    config: dict[str, object]
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Favorite ──────────────────────────────────────────────────────────────

class FavoriteCreateRequest(BaseModel):
    orgId: str
    projectId: str
    icon: str | None = None
    name: str | None = None
    type: str = "PROJECT"


class FavoriteResponse(BaseModel):
    id: str
    orgId: str
    uid: str
    projectId: str
    icon: str | None = None
    name: str | None = None
    type: str
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Vision ────────────────────────────────────────────────────────────────

class VisionCreateRequest(BaseModel):
    projectId: str
    orgId: str
    title: str = Field(min_length=1, max_length=200)
    desc: str = ""
    progress: float = 0.0
    startDate: str | None = None
    endDate: str | None = None
    parentId: str | None = None


class VisionUpdateRequest(BaseModel):
    id: str
    title: str | None = None
    desc: str | None = None
    progress: float | None = None
    startDate: str | None = None
    endDate: str | None = None
    parentId: str | None = None


class VisionResponse(BaseModel):
    id: str
    projectId: str
    orgId: str
    title: str
    desc: str = ""
    progress: float = 0.0
    startDate: str | None = None
    endDate: str | None = None
    parentId: str | None = None
    createdBy: str
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Dashboard ─────────────────────────────────────────────────────────────

class DashboardCreateRequest(BaseModel):
    projectId: str
    title: str = Field(min_length=1, max_length=100)
    isDefault: bool = False


class DashboardComponentCreateRequest(BaseModel):
    dboardId: str
    type: str
    title: str
    icon: str | None = None
    config: dict[str, object] = Field(default_factory=dict)
    x: int = 0
    y: int = 0
    width: int = 4
    height: int = 4


class DashboardComponentLayoutUpdate(BaseModel):
    id: str
    x: int
    y: int
    width: int
    height: int


class DashboardLayoutUpdateRequest(BaseModel):
    components: list[DashboardComponentLayoutUpdate]


class DashboardResponse(BaseModel):
    id: str
    projectId: str
    title: str
    isDefault: bool = False
    createdBy: str
    createdAt: datetime
    updatedAt: datetime | None = None


class DashboardComponentResponse(BaseModel):
    id: str
    dboardId: str
    type: str
    title: str
    icon: str | None = None
    config: dict[str, object]
    x: int = 0
    y: int = 0
    width: int = 4
    height: int = 4
    createdBy: str
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Custom Field ──────────────────────────────────────────────────────────

class FieldCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    type: str
    icon: str | None = None
    order: int = 0
    visible: bool = True
    projectId: str


class FieldUpdateRequest(BaseModel):
    id: str
    name: str | None = None
    icon: str | None = None
    order: int | None = None
    visible: bool | None = None


class FieldSortableRequest(BaseModel):
    items: list[dict[str, object]]


class FieldResponse(BaseModel):
    id: str
    name: str
    type: str
    icon: str | None = None
    order: int = 0
    visible: bool = True
    projectId: str
    createdBy: str
    createdAt: datetime
    updatedAt: datetime | None = None