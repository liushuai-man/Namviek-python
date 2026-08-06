from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, cast

from fastapi import FastAPI, Request
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import get_settings

Document = dict[str, Any]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    client: AsyncMongoClient[Document] = AsyncMongoClient(settings.mongodb_url)
    await client.admin.command("ping")
    database = client[settings.mongodb_database]
    await database.users.create_index("email", unique=True, name="uniq_users_email")
    app.state.mongodb_client = client
    app.state.database = database
    try:
        yield
    finally:
        await client.close()


def get_database(request: Request) -> AsyncDatabase[Document]:
    return cast(AsyncDatabase[Document], request.app.state.database)
