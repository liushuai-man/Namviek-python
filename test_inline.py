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

def test(name, method, path, expected_status, **kwargs):
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
                print(f"        Response: {r.text[:300]}")
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
    if r:
        token = r.headers.get("Authorization", "")
        login_data = r.json()
        user_id = login_data.get("data", {}).get("id", "")
        print(f"        User ID: {user_id}")

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

    # Get Tasks
    test("Get Tasks", "GET", f"/api/project/task?projectId={project_id}", 200, headers=headers)

    # Get Tasks by Query
    test("Query Tasks", "GET", "/api/project/task/query", 200, headers=headers,
         params={"projectId": project_id})

    # Create Checklist
    if task_id:
        test("Create Checklist", "POST", "/api/project/task/checklist", 201, json={
            "taskId": task_id,
            "title": "Test checklist item",
            "order": 0,
        }, headers=headers)

    # Get Checklists
    if task_id:
        test("Get Checklists", "GET", f"/api/project/task/checklist/{task_id}", 200, headers=headers)

    # Create Comment
    if task_id:
        test("Create Comment", "POST", "/api/comment", 201, json={
            "taskId": task_id,
            "content": "Test comment content",
        }, headers=headers)

    # Get Comments
    if task_id:
        test("Get Comments", "GET", f"/api/comment?taskId={task_id}", 200, headers=headers)

    # Get Activities (with objectId)
    test("Get Activities", "GET", "/api/activity", 200, headers=headers,
         params={"objectId": task_id})

    # Create Status (path param)
    test("Create Status", "POST", f"/api/project/status/{project_id}", 201, json={
        "name": "Todo",
        "color": "#FF0000",
        "order": 0,
    }, headers=headers)

    # Get Statuses
    test("Get Statuses", "GET", f"/api/project/status/{project_id}", 200, headers=headers)

    # Create Task Point
    test("Create Point", "POST", "/api/project/point", 201, json={
        "name": "Sprint 1",
        "value": "SP1",
        "order": 0,
        "projectId": project_id,
    }, headers=headers)

    # Get Task Points
    test("Get Points", "GET", f"/api/project/point/{project_id}", 200, headers=headers)

    # Create Tag
    test("Create Tag", "POST", "/api/project/tag", 201, json={
        "name": "Urgent",
        "color": "#FF0000",
        "projectId": project_id,
    }, headers=headers)

    # Get Tags
    test("Get Tags", "GET", f"/api/project/tag/{project_id}", 200, headers=headers)

    # Create Field
    test("Create Field", "POST", "/api/fields", 201, json={
        "name": "Priority",
        "type": "SELECT",
        "projectId": project_id,
        "icon": None,
    }, headers=headers)

    # Get Fields
    test("Get Fields", "GET", f"/api/fields/{project_id}", 200, headers=headers)

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

    # Grid query
    test("Grid Query", "POST", "/api/project/grid/query", 200, json={}, headers=headers)

    # Reorder
    test("Task Reorder", "POST", "/api/task/reorder", 200, json={
        "updatedOrder": [[task_id, 0]],
        "projectId": project_id,
    }, headers=headers)

    # Event task-reorder
    test("Event Task Reorder", "POST", "/api/event/task-reorder", 200, json={
        "updatedOrder": [[task_id, 0]],
        "projectId": project_id,
    }, headers=headers)

    # Status update order
    test("Status Update Order", "PUT", "/api/project/status/order", 200, json={
        "newOrders": [{"id": "", "order": 0}],
    }, headers=headers)

    # Custom field query
    test("Custom Field Query", "POST", "/api/project/task/custom-field/query", 200, json={}, headers=headers)

    # Export
    test("Export Tasks", "GET", "/api/project/task/export", 200, headers=headers,
         params={"projectId": project_id})

    # Counter
    test("Task Counter", "GET", "/api/project/task/counter", 200, headers=headers,
         params={"projectIds": [project_id]})

    # Make cover
    test("Make Cover", "POST", "/api/project/task/make-cover", 200, headers=headers,
         params={"taskId": task_id, "url": "https://example.com/cover.png", "projectId": project_id})

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
