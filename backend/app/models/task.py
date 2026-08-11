from datetime import datetime
from typing import NotRequired, TypedDict

from bson import ObjectId


class TaskDocument(TypedDict):
    _id: ObjectId
    title: str
    desc: str
    projectId: ObjectId
    statusId: ObjectId | None
    priority: str | None
    assigneeIds: list[ObjectId]
    taskStatusId: ObjectId | None
    taskPointId: ObjectId | None
    dueDate: str | None
    startDate: str | None
    done: bool
    order: int
    cover: str | None
    tagIds: list[ObjectId]
    createdBy: ObjectId
    updatedBy: NotRequired[ObjectId | None]
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]
    doneAt: NotRequired[datetime | None]


class TaskChecklistDocument(TypedDict):
    _id: ObjectId
    title: str
    taskId: ObjectId
    done: bool
    doneBy: ObjectId | None
    createdBy: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]
    order: int


class TaskChecklistItemDocument(TypedDict):
    _id: ObjectId
    title: str
    checklistId: ObjectId
    done: bool
    doneBy: ObjectId | None
    createdBy: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]
    order: int


class TaskCommentDocument(TypedDict):
    _id: ObjectId
    content: str
    taskId: ObjectId
    createdBy: ObjectId
    updatedBy: NotRequired[ObjectId | None]
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]


class TaskActivityDocument(TypedDict):
    _id: ObjectId
    objectId: ObjectId
    type: str
    data: dict[str, object]
    createdBy: ObjectId
    createdAt: datetime
    updatedAt: NotRequired[datetime | None]