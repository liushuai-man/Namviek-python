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
    await database.projects.create_index(
        [("organizationId", 1), ("createdAt", -1)],
        name="idx_projects_org_created",
    )
    await database.project_statuses.create_index(
        [("projectId", 1), ("order", 1)],
        name="idx_statuses_project_order",
    )
    await database.project_views.create_index(
        [("projectId", 1), ("order", 1)],
        name="idx_views_project_order",
    )
    await database.tasks.create_index(
        [("projectId", 1), ("order", 1)],
        name="idx_tasks_project_order",
    )
    await database.task_checklists.create_index(
        [("taskId", 1), ("order", 1)],
        name="idx_checklists_task_order",
    )
    await database.task_comments.create_index(
        [("taskId", 1), ("createdAt", -1)],
        name="idx_comments_task_created",
    )
    await database.task_activities.create_index(
        [("objectId", 1), ("createdAt", -1)],
        name="idx_activities_object_created",
    )
    await database.organizations.create_index(
        "slug", unique=True, name="uniq_orgs_slug"
    )
    await database.project_members.create_index(
        [("projectId", 1), ("uid", 1)],
        name="idx_members_project_uid",
    )
    await database.favorites.create_index(
        "orgId", name="idx_favorites_org"
    )
    await database.visions.create_index(
        "projectId", name="idx_visions_project"
    )
    await database.dashboards.create_index(
        "projectId", name="idx_dashboards_project"
    )
    await database.dashboard_components.create_index(
        "dboardId", name="idx_dboard_comp_dboard"
    )
    await database.custom_fields.create_index(
        [("projectId", 1), ("order", 1)],
        name="idx_fields_project_order",
    )
    await database.organization_members.create_index(
        "orgId", name="idx_org_members_org"
    )
    await database.task_automations.create_index(
        "projectId", name="idx_automations_project"
    )
    await database.timers.create_index(
        [("taskId", 1), ("createdAt", -1)],
        name="idx_timers_task_created",
    )
    await database.schedulers.create_index(
        "projectId", name="idx_schedulers_project"
    )
    await database.file_storages.create_index(
        "orgId", name="idx_files_org"
    )
    await database.applications.create_index(
        "orgId", name="idx_apps_org"
    )
    app.state.mongodb_client = client
    app.state.database = database
    try:
        yield
    finally:
        await client.close()


def get_database(request: Request) -> AsyncDatabase[Document]:
    return cast(AsyncDatabase[Document], request.app.state.database)
