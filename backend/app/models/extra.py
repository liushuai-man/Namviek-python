from datetime import datetime
from typing import NotRequired, TypedDict

from bson import ObjectId


class AutomationDocument(TypedDict):
    _id: ObjectId
    projectId: ObjectId
    trigger: dict[str, object]
    action: dict[str, object]
    createdBy: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class TimerDocument(TypedDict):
    _id: ObjectId
    taskId: ObjectId
    createdBy: ObjectId
    startedAt: datetime
    stoppedAt: NotRequired[datetime | None]
    duration: NotRequired[int]
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class SchedulerDocument(TypedDict):
    _id: ObjectId
    organizationId: ObjectId
    projectId: ObjectId
    trigger: dict[str, object]
    action: dict[str, object]
    createdBy: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class MeetingRoomDocument(TypedDict):
    _id: ObjectId
    name: str
    createdBy: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class FileStorageDocument(TypedDict):
    _id: ObjectId
    orgId: ObjectId
    projectId: ObjectId
    name: str
    type: str
    keyName: str
    url: str | None
    createdBy: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class ApplicationDocument(TypedDict):
    _id: ObjectId
    name: str
    desc: str
    orgId: ObjectId
    createdBy: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]