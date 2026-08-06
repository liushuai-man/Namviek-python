from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Literal
from uuid import uuid4

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash

from app.core.errors import AuthorizationError

password_hash = PasswordHash.recommended()
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, password_digest: str) -> bool:
    return password_hash.verify(password, password_digest)


@dataclass(frozen=True, slots=True)
class TokenPayload:
    subject: str
    email: str
    token_type: Literal["access", "refresh"]


class TokenService:
    def __init__(
        self,
        access_secret: str,
        refresh_secret: str,
        access_expire_minutes: int,
        refresh_expire_days: int,
    ) -> None:
        self._access_secret = access_secret
        self._refresh_secret = refresh_secret
        self._access_expire = timedelta(minutes=access_expire_minutes)
        self._refresh_expire = timedelta(days=refresh_expire_days)

    def create_access_token(self, *, user_id: str, email: str) -> str:
        return self._encode(
            user_id=user_id,
            email=email,
            token_type="access",
            secret=self._access_secret,
            expires_delta=self._access_expire,
        )

    def create_refresh_token(self, *, user_id: str, email: str) -> str:
        return self._encode(
            user_id=user_id,
            email=email,
            token_type="refresh",
            secret=self._refresh_secret,
            expires_delta=self._refresh_expire,
        )

    def decode_access_token(self, token: str) -> TokenPayload:
        return self._decode(token, self._access_secret, "access")

    def decode_refresh_token(self, token: str) -> TokenPayload:
        return self._decode(token, self._refresh_secret, "refresh")

    @staticmethod
    def _encode(
        *,
        user_id: str,
        email: str,
        token_type: Literal["access", "refresh"],
        secret: str,
        expires_delta: timedelta,
    ) -> str:
        now = datetime.now(UTC)
        return jwt.encode(
            {
                "sub": user_id,
                "email": email,
                "type": token_type,
                "iat": now,
                "exp": now + expires_delta,
                "jti": str(uuid4()),
            },
            secret,
            algorithm=ALGORITHM,
        )

    @staticmethod
    def _decode(
        token: str,
        secret: str,
        expected_type: Literal["access", "refresh"],
    ) -> TokenPayload:
        try:
            payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
            subject = payload.get("sub")
            email = payload.get("email")
            token_type = payload.get("type")
            if (
                not isinstance(subject, str)
                or not isinstance(email, str)
                or token_type != expected_type
            ):
                raise AuthorizationError("Invalid token payload")
            return TokenPayload(subject, email, expected_type)
        except ExpiredSignatureError as error:
            raise AuthorizationError("Token has expired") from error
        except InvalidTokenError as error:
            raise AuthorizationError("Invalid token") from error

