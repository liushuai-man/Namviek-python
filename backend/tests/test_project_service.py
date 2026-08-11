import pytest
from bson import ObjectId

from app.schemas.project import (
    ProjectCreateRequest,
    ProjectViewCreateRequest,
    ProjectViewType,
)
from app.services.project_service import ProjectService
from tests.fakes import FakeProjectRepository


def _make_org_id() -> str:
    return str(ObjectId())


def _make_user_id() -> str:
    return str(ObjectId())


@pytest.mark.asyncio
async def test_create_project_creates_default_statuses() -> None:
    repo = FakeProjectRepository()
    service = ProjectService(repo)

    result = await service.create_project(
        ProjectCreateRequest(
            name="Test Project",
            desc="",
            organizationId=_make_org_id(),
        ),
        _make_user_id(),
    )

    assert result.name == "Test Project"
    statuses = await service.get_statuses(result.id)
    assert len(statuses) == 3
    assert statuses[0].name == "Todo"
    assert statuses[1].name == "In Progress"
    assert statuses[2].name == "Done"


@pytest.mark.asyncio
async def test_get_projects_by_org() -> None:
    repo = FakeProjectRepository()
    service = ProjectService(repo)
    org_id = _make_org_id()
    user_id = _make_user_id()

    await service.create_project(
        ProjectCreateRequest(name="A", desc="", organizationId=org_id), user_id
    )
    await service.create_project(
        ProjectCreateRequest(name="B", desc="", organizationId=org_id), user_id
    )

    projects = await service.get_projects(org_id)
    assert len(projects) == 2


@pytest.mark.asyncio
async def test_archive_project() -> None:
    repo = FakeProjectRepository()
    service = ProjectService(repo)
    user_id = _make_user_id()

    project = await service.create_project(
        ProjectCreateRequest(name="X", desc="", organizationId=_make_org_id()), user_id
    )

    archived = await service.archive_project(project.id, archived=True, user_id=user_id)
    assert archived.archivedAt is not None

    active = await service.get_projects(project.organizationId, is_archived=False)
    assert len(active) == 0


@pytest.mark.asyncio
async def test_create_and_get_views() -> None:
    repo = FakeProjectRepository()
    service = ProjectService(repo)
    user_id = _make_user_id()

    project = await service.create_project(
        ProjectCreateRequest(name="P", desc="", organizationId=_make_org_id()), user_id
    )

    view = await service.create_view(
        ProjectViewCreateRequest(
            name="Board",
            type=ProjectViewType.BOARD,
            projectId=project.id,
        )
    )
    assert view.name == "Board"

    views = await service.get_views(project.id)
    assert len(views) == 1
    assert views[0].id == view.id


@pytest.mark.asyncio
async def test_delete_view() -> None:
    repo = FakeProjectRepository()
    service = ProjectService(repo)
    user_id = _make_user_id()

    project = await service.create_project(
        ProjectCreateRequest(name="P", desc="", organizationId=_make_org_id()), user_id
    )

    view = await service.create_view(
        ProjectViewCreateRequest(
            name="List",
            type=ProjectViewType.LIST,
            projectId=project.id,
        )
    )

    await service.delete_view(view.id)
    views = await service.get_views(project.id)
    assert len(views) == 0