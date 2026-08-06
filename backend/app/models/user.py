from datetime import datetime
from typing import NotRequired, TypedDict

from bson import ObjectId


class UserDocument(TypedDict):
    _id: ObjectId
    email: str
    password_hash: str
    name: str
    status: str
    photo: str | None
    settings: dict[str, object]
    created_at: datetime
    updated_at: NotRequired[datetime | None]

