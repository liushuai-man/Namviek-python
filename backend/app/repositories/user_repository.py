from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Protocol, cast

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.errors import DuplicateKeyError

from app.core.errors import ConflictError
from app.db.mongodb import Document
from app.models.user import UserDocument


class UserRepositoryProtocol(Protocol):
    async def create(
        self, *, email: str, password_hash: str, name: str
    ) -> UserDocument: ...

    async def find_by_email(self, email: str) -> UserDocument | None: ...

    async def find_by_id(self, user_id: str) -> UserDocument | None: ...


class MongoUserRepository:
    def __init__(self, database: AsyncDatabase[Document]) -> None:
        self._collection = database.users

    async def create(
        self, *, email: str, password_hash: str, name: str
    ) -> UserDocument:
        document: Document = {
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "status": "ACTIVE",
            "photo": None,
            "settings": {},
            "created_at": datetime.now(UTC),
            "updated_at": None,
        }
        try:
            result = await self._collection.insert_one(document)
        except DuplicateKeyError as error:
            raise ConflictError("Email already exists") from error
        document["_id"] = result.inserted_id
        return _as_user_document(document)

    async def find_by_email(self, email: str) -> UserDocument | None:
        document = await self._collection.find_one({"email": email})
        return _as_user_document(document) if document else None

    async def find_by_id(self, user_id: str) -> UserDocument | None:
        try:
            object_id = ObjectId(user_id)
        except InvalidId:
            return None
        document = await self._collection.find_one({"_id": object_id})
        return _as_user_document(document) if document else None


def _as_user_document(document: Mapping[str, object]) -> UserDocument:
    return cast(UserDocument, dict(document))

