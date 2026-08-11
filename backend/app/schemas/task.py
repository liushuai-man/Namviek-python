from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class TaskPriority(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


# ── Task ─────────────────────────────────────────────────────────────────

class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    desc: str = ""
    projectId: str
    statusId: str | None = None
    priority: str | None = None
    assigneeIds: list[str] = Field(default_factory=list)
    taskStatusId: str | None = None
    taskPointId: str | None = None
    dueDate: str | None = None
    startDate: str | None = None
    done: bool = False
    order: int = 0
    tagIds: list[str] = Field(default_factory=list)


class TaskUpdateRequest(BaseModel):
    id: str
    title: str | None = None
    desc: str | None = None
    statusId: str | None = None
    priority: str | None = None
    assigneeIds: list[str] | None = None
    taskStatusId: str | None = None
    taskPointId: str | None = None
    dueDate: str | None = None
    startDate: str | None = None
    done: bool | None = None
    order: int | None = None
    cover: str | None = None
    tagIds: list[str] | None = None


class TaskUpdateManyRequest(BaseModel):
    ids: list[str]
    data: TaskUpdateRequest


class TaskAddManyRequest(BaseModel):
    data: list[TaskCreateRequest]
    projectId: str


class TaskReorderRequest(BaseModel):
    updatedOrder: list[list[str | int]]
    projectId: str


class TaskQueryRequest(BaseModel):
    projectId: str | None = None
    projectIds: list[str] | None = None
    title: str | None = None
    dueDate: list[str] | None = None
    assigneeIds: list[str] | None = None
    statusIds: list[str] | None = None
    taskPoint: int | None = None
    priority: str | None = None
    done: str | None = None
    take: int | None = None
    skip: int | None = None
    orderBy: list[str] | None = None
    counter: bool | None = None


class TaskResponse(BaseModel):
    id: str
    title: str
    desc: str
    projectId: str
    statusId: str | None = None
    priority: str | None = None
    assigneeIds: list[str] = Field(default_factory=list)
    taskStatusId: str | None = None
    taskPointId: str | None = None
    dueDate: str | None = None
    startDate: str | None = None
    done: bool = False
    order: int = 0
    cover: str | None = None
    tagIds: list[str] = Field(default_factory=list)
    createdBy: str
    updatedBy: str | None = None
    createdAt: datetime
    updatedAt: datetime | None = None
    doneAt: datetime | None = None


# ── Task Checklist ────────────────────────────────────────────────────────

class ChecklistCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    taskId: str
    done: bool = False
    doneBy: str | None = None
    order: int = 0


class ChecklistUpdateRequest(BaseModel):
    id: str
    title: str | None = None
    done: bool | None = None
    doneBy: str | None = None
    order: int | None = None


class ChecklistResponse(BaseModel):
    id: str
    title: str
    taskId: str
    done: bool = False
    doneBy: str | None = None
    createdBy: str
    createdAt: datetime
    updatedAt: datetime | None = None
    order: int = 0


# ── Comment ───────────────────────────────────────────────────────────────

class CommentCreateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=5000)
    taskId: str


class CommentUpdateRequest(BaseModel):
    id: str
    content: str | None = None


class CommentResponse(BaseModel):
    id: str
    content: str
    taskId: str
    createdBy: str
    updatedBy: str | None = None
    createdAt: datetime
    updatedAt: datetime | None = None


# ── Activity ──────────────────────────────────────────────────────────────

class ActivityCreateRequest(BaseModel):
    type: str
    data: dict[str, object] = Field(default_factory=dict)


class ActivityUpdateRequest(BaseModel):
    id: str
    data: dict[str, object] | None = None


class ActivityResponse(BaseModel):
    id: str
    objectId: str
    type: str
    data: dict[str, object]
    createdBy: str
    createdAt: datetime
    updatedAt: datetime | None = None