from typing import Annotated

from fastapi import APIRouter, Header, Response, status

from app.api.dependencies import AuthServiceDependency, CurrentUser
from app.core.errors import AuthorizationError
from app.schemas.auth import (
    AuthResponse,
    RefreshTokenRequest,
    SignInRequest,
    SignUpRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/sign-up",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up(
    data: SignUpRequest,
    service: AuthServiceDependency,
) -> AuthResponse:
    user = await service.sign_up(data)
    return AuthResponse(status=200, data=user)


@router.post("/sign-in", response_model=AuthResponse)
async def sign_in(
    data: SignInRequest,
    response: Response,
    service: AuthServiceDependency,
) -> AuthResponse:
    result = await service.sign_in(data)
    _set_token_headers(response, result.tokens)
    return AuthResponse(data=result.user)


@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(
    response: Response,
    service: AuthServiceDependency,
    data: RefreshTokenRequest | None = None,
    refresh_token_header: Annotated[str | None, Header(alias="RefreshToken")] = None,
) -> TokenResponse:
    token = (data.refresh_token if data else None) or refresh_token_header
    if not token:
        raise AuthorizationError("Refresh token is required")
    result = await service.refresh(token)
    _set_token_headers(response, result.tokens)
    return result.tokens


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser) -> UserResponse:
    return current_user


def _set_token_headers(response: Response, tokens: TokenResponse) -> None:
    # Raw tokens preserve the existing Namviek frontend contract. New clients may
    # send the access token as `Authorization: Bearer <token>` as well.
    response.headers["Authorization"] = tokens.access_token
    response.headers["RefreshToken"] = tokens.refresh_token
