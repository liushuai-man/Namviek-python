import pytest

from app.core.errors import AuthenticationError, ConflictError
from app.core.security import TokenService
from app.schemas.auth import SignInRequest, SignUpRequest
from app.services.auth_service import AuthService
from tests.fakes import FakeUserRepository


def build_service() -> tuple[AuthService, FakeUserRepository]:
    repository = FakeUserRepository()
    tokens = TokenService(
        access_secret="test-access-secret-with-enough-entropy",
        refresh_secret="test-refresh-secret-with-enough-entropy",
        access_expire_minutes=30,
        refresh_expire_days=4,
    )
    return AuthService(repository, tokens, registration_enabled=True), repository


@pytest.mark.asyncio
async def test_sign_up_hashes_password_and_normalizes_email() -> None:
    service, repository = build_service()

    user = await service.sign_up(
        SignUpRequest(email="Learner@Example.com", password="secret123", name="Learner")
    )

    stored = repository.users["learner@example.com"]
    assert user.email == "learner@example.com"
    assert stored["password_hash"] != "secret123"
    assert stored["password_hash"].startswith("$argon2")


@pytest.mark.asyncio
async def test_duplicate_email_is_rejected() -> None:
    service, _repository = build_service()
    data = SignUpRequest(
        email="learner@example.com", password="secret123", name="Learner"
    )
    await service.sign_up(data)

    with pytest.raises(ConflictError):
        await service.sign_up(data)


@pytest.mark.asyncio
async def test_sign_in_and_refresh_create_token_pairs() -> None:
    service, _repository = build_service()
    await service.sign_up(
        SignUpRequest(email="learner@example.com", password="secret123", name="Learner")
    )

    signed_in = await service.sign_in(
        SignInRequest(email="learner@example.com", password="secret123")
    )
    refreshed = await service.refresh(signed_in.tokens.refresh_token)

    assert signed_in.tokens.access_token
    assert signed_in.tokens.refresh_token
    assert refreshed.user.id == signed_in.user.id
    assert refreshed.tokens.access_token != signed_in.tokens.access_token


@pytest.mark.asyncio
async def test_wrong_password_is_rejected() -> None:
    service, _repository = build_service()
    await service.sign_up(
        SignUpRequest(email="learner@example.com", password="secret123", name="Learner")
    )

    with pytest.raises(AuthenticationError):
        await service.sign_in(
            SignInRequest(email="learner@example.com", password="wrong-password")
        )
