from datetime import datetime
from typing import NotRequired, TypedDict

from bson import ObjectId


class ProjectDocument(TypedDict):
    _id: ObjectId
    name: str
    desc: str
    icon: str | None
    color: str | None
    cover: str | None
    organizationId: ObjectId
    createdBy: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]
    archivedAt: NotRequired[datetime | None]
    archivedBy: NotRequired[ObjectId | None]
    allMemberVisible: bool


class ProjectStatusDocument(TypedDict):
    _id: ObjectId
    name: str
    color: str | None
    order: int
    projectId: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class ProjectViewDocument(TypedDict):
    _id: ObjectId
    name: str
    type: str
    icon: str | None
    order: int
    data: dict[str, object]
    projectId: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]
    pinned: bool


class ProjectPointDocument(TypedDict):
    _id: ObjectId
    name: str
    value: str
    icon: str | None
    order: int
    projectId: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class ProjectTagDocument(TypedDict):
    _id: ObjectId
    name: str
    color: str | None
    projectId: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class ProjectMemberDocument(TypedDict):
    _id: ObjectId
    projectId: ObjectId
    uid: ObjectId
    role: str
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]