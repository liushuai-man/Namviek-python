from datetime import datetime
from typing import NotRequired, TypedDict

from bson import ObjectId


class OrganizationDocument(TypedDict):
    _id: ObjectId
    name: str
    slug: str
    description: str
    cover: str | None
    logo: str | None
    createdBy: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class OrganizationStorageDocument(TypedDict):
    _id: ObjectId
    orgId: ObjectId
    type: str
    config: dict[str, object]
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class FavoriteDocument(TypedDict):
    _id: ObjectId
    orgId: ObjectId
    uid: ObjectId
    projectId: ObjectId
    icon: str | None
    name: str | None
    type: str
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class VisionDocument(TypedDict):
    _id: ObjectId
    projectId: ObjectId
    orgId: ObjectId
    title: str
    desc: str
    progress: float
    startDate: str | None
    endDate: str | None
    parentId: ObjectId | None
    createdBy: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class DashboardDocument(TypedDict):
    _id: ObjectId
    projectId: ObjectId
    title: str
    isDefault: bool
    createdBy: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class DashboardComponentDocument(TypedDict):
    _id: ObjectId
    dboardId: ObjectId
    type: str
    title: str
    icon: str | None
    config: dict[str, object]
    x: int
    y: int
    width: int
    height: int
    createdBy: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class CustomFieldDocument(TypedDict):
    _id: ObjectId
    name: str
    type: str
    icon: str | None
    order: int
    visible: bool
    projectId: ObjectId
    createdBy: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]