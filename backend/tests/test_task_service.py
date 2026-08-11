import pytest
from bson import ObjectId

from app.schemas.task import (
    ChecklistCreateRequest,
    ChecklistUpdateRequest,
    CommentCreateRequest,
    CommentUpdateRequest,
    TaskCreateRequest,
    TaskUpdateRequest,
)
from app.services.task_service import TaskService
from tests.fakes import FakeTaskRepository


def _make_id() -> str:
    return str(ObjectId())


@pytest.mark.asyncio
async def test_create_and_get_task() -> None:
    repo = FakeTaskRepository()
    service = TaskService(repo)

    task = await service.create_task(
        TaskCreateRequest(title="Test Task", projectId=_make_id()),
        _make_id(),
    )
    assert task.title == "Test Task"
    assert task.done is False

    tasks = await service.get_tasks(task.projectId)
    assert len(tasks) == 1
    assert tasks[0].id == task.id


@pytest.mark.asyncio
async def test_update_task() -> None:
    repo = FakeTaskRepository()
    service = TaskService(repo)
    user_id = _make_id()

    task = await service.create_task(
        TaskCreateRequest(title="Old Title", projectId=_make_id()),
        user_id,
    )
    updated = await service.update_task(
        TaskUpdateRequest(id=task.id, title="New Title", done=True), user_id
    )
    assert updated.title == "New Title"
    assert updated.done is True


@pytest.mark.asyncio
async def test_delete_task() -> None:
    repo = FakeTaskRepository()
    service = TaskService(repo)

    task = await service.create_task(
        TaskCreateRequest(title="To Delete", projectId=_make_id()),
        _make_id(),
    )
    await service.delete_task(task.id)
    tasks = await service.get_tasks(task.projectId)
    assert len(tasks) == 0


@pytest.mark.asyncio
async def test_reorder_tasks() -> None:
    repo = FakeTaskRepository()
    service = TaskService(repo)
    project_id = _make_id()
    user_id = _make_id()

    t1 = await service.create_task(
        TaskCreateRequest(title="A", projectId=project_id, order=0), user_id
    )
    t2 = await service.create_task(
        TaskCreateRequest(title="B", projectId=project_id, order=1), user_id
    )

    from app.schemas.task import TaskReorderRequest
    await service.reorder_tasks(
        TaskReorderRequest(
            updatedOrder=[[t1.id, 5], [t2.id, 3]],
            projectId=project_id,
        )
    )

    tasks = await service.get_tasks(project_id)
    orders = {t.title: t.order for t in tasks}
    assert orders["A"] == 5
    assert orders["B"] == 3


@pytest.mark.asyncio
async def test_create_and_get_checklist() -> None:
    repo = FakeTaskRepository()
    service = TaskService(repo)
    user_id = _make_id()

    task = await service.create_task(
        TaskCreateRequest(title="Task", projectId=_make_id()), user_id
    )

    cl = await service.create_checklist(
        ChecklistCreateRequest(title="Step 1", taskId=task.id), user_id
    )
    assert cl.title == "Step 1"

    items = await service.get_checklists(task.id)
    assert len(items) == 1


@pytest.mark.asyncio
async def test_update_checklist_done() -> None:
    repo = FakeTaskRepository()
    service = TaskService(repo)
    user_id = _make_id()

    task = await service.create_task(
        TaskCreateRequest(title="Task", projectId=_make_id()), user_id
    )
    cl = await service.create_checklist(
        ChecklistCreateRequest(title="Step 1", taskId=task.id), user_id
    )

    updated = await service.update_checklist(
        ChecklistUpdateRequest(id=cl.id, done=True, doneBy=user_id)
    )
    assert updated.done is True


@pytest.mark.asyncio
async def test_create_and_get_comment() -> None:
    repo = FakeTaskRepository()
    service = TaskService(repo)
    user_id = _make_id()

    task = await service.create_task(
        TaskCreateRequest(title="Task", projectId=_make_id()), user_id
    )

    comment = await service.create_comment(
        CommentCreateRequest(content="Hello", taskId=task.id), user_id
    )
    assert comment.content == "Hello"

    comments = await service.get_comments(task.id)
    assert len(comments) == 1


@pytest.mark.asyncio
async def test_update_comment() -> None:
    repo = FakeTaskRepository()
    service = TaskService(repo)
    user_id = _make_id()

    task = await service.create_task(
        TaskCreateRequest(title="Task", projectId=_make_id()), user_id
    )
    comment = await service.create_comment(
        CommentCreateRequest(content="Old", taskId=task.id), user_id
    )

    updated = await service.update_comment(
        CommentUpdateRequest(id=comment.id, content="New"), user_id
    )
    assert updated.content == "New"