import os
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient

from app.core.config import get_settings
from app.main import app

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.getenv("RUN_MONGODB_TESTS") != "1",
        reason="set RUN_MONGODB_TESTS=1 to run MongoDB integration tests",
    ),
]


def test_register_and_sign_in_with_real_mongodb() -> None:
    settings = get_settings()
    email = f"auth-test-{uuid4().hex}@example.com"
    sync_client: MongoClient[dict[str, object]] = MongoClient(settings.mongodb_url)
    users = sync_client[settings.mongodb_database].users

    try:
        with TestClient(app) as client:
            sign_up = client.post(
                "/api/auth/sign-up",
                json={"email": email, "password": "secret123", "name": "Test User"},
            )
            assert sign_up.status_code == 201

            sign_in = client.post(
                "/api/auth/sign-in",
                json={"email": email, "password": "secret123"},
            )
            assert sign_in.status_code == 200
            assert sign_in.headers["authorization"]
            assert sign_in.headers["refreshtoken"]
    finally:
        users.delete_one({"email": email})
        sync_client.close()

