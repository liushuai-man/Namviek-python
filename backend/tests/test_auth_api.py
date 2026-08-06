from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_auth_service
from app.core.security import TokenService
from app.main import app
from app.services.auth_service import AuthService
from tests.fakes import FakeUserRepository


@pytest.fixture
def client() -> Iterator[TestClient]:
    service = AuthService(
        FakeUserRepository(),
        TokenService(
            access_secret="test-access-secret-with-enough-entropy",
            refresh_secret="test-refresh-secret-with-enough-entropy",
            access_expire_minutes=30,
            refresh_expire_days=4,
        ),
        registration_enabled=True,
    )
    app.dependency_overrides[get_auth_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_complete_email_password_auth_flow(client: TestClient) -> None:
    sign_up = client.post(
        "/api/auth/sign-up",
        json={
            "email": "learner@example.com",
            "password": "secret123",
            "name": "Learner",
        },
    )
    assert sign_up.status_code == 201
    assert sign_up.json()["data"]["email"] == "learner@example.com"

    sign_in = client.post(
        "/api/auth/sign-in",
        json={
            "email": "learner@example.com",
            "password": "secret123",
            "provider": "EMAIL_PASSWORD",
        },
    )
    assert sign_in.status_code == 200
    access_token = sign_in.headers["authorization"]
    refresh_token = sign_in.headers["refreshtoken"]

    current_user = client.get(
        "/api/auth/me", headers={"Authorization": access_token}
    )
    assert current_user.status_code == 200
    assert current_user.json()["name"] == "Learner"
    assert current_user.headers["x-content-type-options"] == "nosniff"

    refreshed = client.post(
        "/api/auth/refresh-token", headers={"RefreshToken": refresh_token}
    )
    assert refreshed.status_code == 200
    assert refreshed.json()["access_token"]
    assert refreshed.headers["authorization"]


def test_me_requires_authentication(client: TestClient) -> None:
    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "not_authenticated"

