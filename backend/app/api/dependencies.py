from typing import Annotated

from fastapi import Depends, Header
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import Settings, get_settings
from app.core.errors import AuthorizationError
from app.core.security import TokenService
from app.db.mongodb import Document, get_database
from app.repositories.user_repository import MongoUserRepository
from app.schemas.auth import UserResponse
from app.services.auth_service import AuthService

DatabaseDependency = Annotated[AsyncDatabase[Document], Depends(get_database)]
SettingsDependency = Annotated[Settings, Depends(get_settings)]


def get_token_service(settings: SettingsDependency) -> TokenService:
    return TokenService(
        access_secret=settings.jwt_secret_key.get_secret_value(),
        refresh_secret=settings.jwt_refresh_key.get_secret_value(),
        access_expire_minutes=settings.access_token_expire_minutes,
        refresh_expire_days=settings.refresh_token_expire_days,
    )


def get_auth_service(
    database: DatabaseDependency,
    settings: SettingsDependency,
    token_service: Annotated[TokenService, Depends(get_token_service)],
) -> AuthService:
    return AuthService(
        MongoUserRepository(database),
        token_service,
        registration_enabled=settings.registration_enabled,
    )


AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]


async def get_current_user(
    service: AuthServiceDependency,
    authorization: Annotated[str | None, Header()] = None,
) -> UserResponse:
    if not authorization:
        raise AuthorizationError
    token = authorization.removeprefix("Bearer ").removeprefix("bearer ").strip()
    if not token:
        raise AuthorizationError
    return await service.get_user_from_access_token(token)


CurrentUser = Annotated[UserResponse, Depends(get_current_user)]

