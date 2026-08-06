from enum import StrEnum

from pydantic import BaseModel, EmailStr, Field


class UserStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class AuthProvider(StrEnum):
    EMAIL_PASSWORD = "EMAIL_PASSWORD"
    GOOGLE = "GOOGLE"


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4, max_length=100)
    name: str = Field(min_length=2, max_length=30)


class SignInRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=1000)
    provider: AuthProvider = AuthProvider.EMAIL_PASSWORD


class RefreshTokenRequest(BaseModel):
    refresh_token: str | None = None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    status: UserStatus
    photo: str | None = None


class AuthResponse(BaseModel):
    status: int = 200
    data: UserResponse


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

