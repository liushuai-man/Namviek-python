from datetime import UTC, datetime

from bson import ObjectId

from app.models.user import UserDocument


class FakeUserRepository:
    def __init__(self) -> None:
        self.users: dict[str, UserDocument] = {}

    async def create(
        self, *, email: str, password_hash: str, name: str
    ) -> UserDocument:
        user: UserDocument = {
            "_id": ObjectId(),
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "status": "ACTIVE",
            "photo": None,
            "settings": {},
            "created_at": datetime.now(UTC),
            "updated_at": None,
        }
        self.users[email] = user
        return user

    async def find_by_email(self, email: str) -> UserDocument | None:
        return self.users.get(email)

    async def find_by_id(self, user_id: str) -> UserDocument | None:
        return next(
            (user for user in self.users.values() if str(user["_id"]) == user_id),
            None,
        )

