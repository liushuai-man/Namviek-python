"""Integration test - tests the complete API flow."""
import os
import subprocess
import sys
import time

import httpx

os.environ["NAMVIEK_MONGO_URI"] = "mongodb://localhost:27017/namviek?replicaSet=rs0"

proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

time.sleep(5)

if proc.poll() is not None:
    print("Backend failed to start")
    sys.exit(1)

print("=== Backend started on port 8000 ===\n")

BASE = "http://127.0.0.1:8000"
client = httpx.Client(timeout=30)

passed = 0
failed = 0

def test(name: str, method: str, path: str, expected_status: int, **kwargs):
    global passed, failed
    url = f"{BASE}{path}"
    try:
        if method == "GET":
            r = client.get(url, **kwargs)
        elif method == "POST":
            r = client.post(url, **kwargs)
        elif method == "PUT":
            r = client.put(url, **kwargs)
        elif method == "DELETE":
            r = client.delete(url, **kwargs)
        else:
            return
        if r.status_code == expected_status:
            print(f"  PASS  {name} => {r.status_code}")
            passed += 1
            return r
        else:
            print(f"  FAIL  {name} => expected {expected_status}, got {r.status_code}")
            if r.text:
                print(f"        Response: {r.text[:200]}")
            failed += 1
            return r
    except Exception as e:
        print(f"  FAIL  {name} => {e}")
        failed += 1
        return None

try:
    unique_id = str(int(time.time()))

    # Health check
    test("Health", "GET", "/api/v1/health", 200)

    # Register
    r = test("Register", "POST", "/api/auth/sign-up", 201, json={
        "email": f"test{unique_id}@example.com",
        "password": "Test1234!",
        "name": f"Test User {unique_id}",
    })

    # Login
    r = test("Login", "POST", "/api/auth/sign-in", 200, json={
        "email": f"test{unique_id}@example.com",
        "password": "Test1234!",
        "provider": "EMAIL_PASSWORD",
    })

    token = ""
    refresh_token = ""
    if r:
        token = r.headers.get("Authorization", "")
        refresh_token = r.headers.get("RefreshToken", "")
        login_data = r.json()
        user_id = login_data.get("data", {}).get("id", "")
        print(f"        User ID: {user_id}")
        print(f"        Token: {token[:50]}...")

    headers = {"Authorization": f"Bearer {token}"} if token else {}

    # Create Organization
    r = test("Create Org", "POST", "/api/org", 201, json={
        "name": f"Test Org {unique_id}",
        "desc": "Test organization",
    }, headers=headers)

    org_id = ""
    if r:
        org_data = r.json()
        org_id = org_data.get("id", "")
        print(f"        Org ID: {org_id}")

    # Get Organizations
    test("Get Orgs", "GET", "/api/org", 200, headers=headers)

    # Create Project
    r = test("Create Project", "POST", "/api/project", 201, json={
        "name": f"Test Project {unique_id}",
        "desc": "Test project",
        "orgId": org_id,
        "views": ["BOARD", "LIST"],
    }, headers=headers)

    project_id = ""
    if r:
        project_data = r.json()
        project_id = project_data.get("id", "")
        print(f"        Project ID: {project_id}")

    # Get Projects
    test("Get Projects", "GET", f"/api/project?orgId={org_id}", 200, headers=headers)

    # Get Project Views
    test("Get Views", "GET", f"/api/project-view?projectId={project_id}", 200, headers=headers)

    # Create Task
    r = test("Create Task", "POST", "/api/project/task", 201, json={
        "title": f"Test Task {unique_id}",
        "projectId": project_id,
        "desc": "Test task description",
    }, headers=headers)

    task_id = ""
    if r:
        task_data = r.json()
        task_id = task_data.get("id", "")
        print(f"        Task ID: {task_id}")

    # Get Tasks
    test("Get Tasks", "GET", f"/api/project/task?projectId={project_id}", 200, headers=headers)

    # Get Tasks by Query
    test("Query Tasks", "GET", f"/api/project/task/query", 200, headers=headers,
         params={"projectId": project_id})

    # Create Checklist
    if task_id:
        test("Create Checklist", "POST", "/api/checklist", 201, json={
            "taskId": task_id,
            "title": "Test checklist item",
            "order": 0,
        }, headers=headers)

    # Get Checklists
    if task_id:
        test("Get Checklists", "GET", f"/api/checklist?taskId={task_id}", 200, headers=headers)

    # Create Comment
    if task_id:
        test("Create Comment", "POST", "/api/comment", 201, json={
            "taskId": task_id,
            "content": "Test comment content",
        }, headers=headers)

    # Get Comments
    if task_id:
        test("Get Comments", "GET", f"/api/comment?taskId={task_id}", 200, headers=headers)

    # Get Activities
    test("Get Activities", "GET", "/api/activity", 200, headers=headers)

    # Create Status
    r = test("Create Status", "POST", "/api/project-status", 201, json={
        "name": "Todo",
        "color": "#FF0000",
        "order": 0,
        "projectId": project_id,
    }, headers=headers)

    # Get Statuses
    test("Get Statuses", "GET", f"/api/project-status?projectId={project_id}", 200, headers=headers)

    # Create Task Point
    r = test("Create Point", "POST", "/api/project-point", 201, json={
        "name": "Sprint 1",
        "value": "SP1",
        "order": 0,
        "projectId": project_id,
    }, headers=headers)

    # Get Task Points
    test("Get Points", "GET", f"/api/project-point?projectId={project_id}", 200, headers=headers)

    # Create Tag
    test("Create Tag", "POST", "/api/project-tag", 201, json={
        "name": "Urgent",
        "color": "#FF0000",
        "projectId": project_id,
    }, headers=headers)

    # Get Tags
    test("Get Tags", "GET", f"/api/project-tag?projectId={project_id}", 200, headers=headers)

    # Create Field
    test("Create Field", "POST", "/api/field", 201, json={
        "name": "Priority",
        "type": "SELECT",
        "projectId": project_id,
        "icon": None,
    }, headers=headers)

    # Get Fields
    test("Get Fields", "GET", f"/api/field?projectId={project_id}", 200, headers=headers)

    # Pin Project
    test("Pin Project", "POST", "/api/project/pin", 200, json={
        "projectId": project_id,
    }, headers=headers)

    # Get Pinned
    test("Get Pinned", "GET", "/api/project/pin", 200, headers=headers)

    # Archive Project
    test("Archive Project", "POST", "/api/project/archive", 200, json={
        "projectId": project_id,
        "archive": True,
    }, headers=headers)

    # Get Me
    test("Get Me", "GET", "/api/auth/me", 200, headers=headers)

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    if failed == 0:
        print("ALL TESTS PASSED!")
    else:
        print(f"{failed} TESTS FAILED!")

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    proc.terminate()
    proc.wait()
    client.close()
