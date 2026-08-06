from dataclasses import dataclass

from app.core.errors import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    RegistrationDisabledError,
    UnsupportedAuthProviderError,
)
from app.core.security import TokenService, hash_password, verify_password
from app.models.user import UserDocument
from app.repositories.user_repository import UserRepositoryProtocol
from app.schemas.auth import (
    AuthProvider,
    SignInRequest,
    SignUpRequest,
    TokenResponse,
    UserResponse,
    UserStatus,
)


@dataclass(frozen=True, slots=True)
class AuthResult:
    user: UserResponse
    tokens: TokenResponse


class AuthService:
    def __init__(
        self,
        repository: UserRepositoryProtocol,
        token_service: TokenService,
        *,
        registration_enabled: bool,
    ) -> None:
        self._repository = repository
        self._tokens = token_service
        self._registration_enabled = registration_enabled

    async def sign_up(self, data: SignUpRequest) -> UserResponse:
        if not self._registration_enabled:
            raise RegistrationDisabledError
        email = data.email.lower()
        if await self._repository.find_by_email(email):
            raise ConflictError("Email already exists")
        user = await self._repository.create(
            email=email,
            password_hash=hash_password(data.password),
            name=data.name.strip(),
        )
        return self._to_response(user)

    async def sign_in(self, data: SignInRequest) -> AuthResult:
        if data.provider is not AuthProvider.EMAIL_PASSWORD:
            raise UnsupportedAuthProviderError
        user = await self._repository.find_by_email(data.email.lower())
        if user is None or not verify_password(data.password, user["password_hash"]):
            raise AuthenticationError
        if user["status"] != UserStatus.ACTIVE:
            raise AuthenticationError("Account is inactive")
        response = self._to_response(user)
        return AuthResult(response, self._create_token_pair(response))

    async def refresh(self, refresh_token: str) -> AuthResult:
        payload = self._tokens.decode_refresh_token(refresh_token)
        user = await self._repository.find_by_id(payload.subject)
        if user is None or user["email"] != payload.email:
            raise AuthorizationError("Refresh token user no longer exists")
        response = self._to_response(user)
        return AuthResult(response, self._create_token_pair(response))

    async def get_user_from_access_token(self, access_token: str) -> UserResponse:
        payload = self._tokens.decode_access_token(access_token)
        user = await self._repository.find_by_id(payload.subject)
        if user is None or user["email"] != payload.email:
            raise AuthorizationError("Token user no longer exists")
        return self._to_response(user)

    def _create_token_pair(self, user: UserResponse) -> TokenResponse:
        return TokenResponse(
            access_token=self._tokens.create_access_token(
                user_id=user.id, email=str(user.email)
            ),
            refresh_token=self._tokens.create_refresh_token(
                user_id=user.id, email=str(user.email)
            ),
        )

    @staticmethod
    def _to_response(user: UserDocument) -> UserResponse:
        return UserResponse(
            id=str(user["_id"]),
            email=user["email"],
            name=user["name"],
            status=UserStatus(user["status"]),
            photo=user["photo"],
        )
