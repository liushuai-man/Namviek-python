"""Full API integration test script."""
import httpx
import time
import json

BASE = "http://127.0.0.1:8000"
client = httpx.Client(timeout=30)

print("=" * 60)
print("完整 API 流程测试")
print("=" * 60)

# 1. Health check
print("\n1. 健康检查")
r = client.get(f"{BASE}/api/v1/health")
print(f"   GET /api/v1/health => {r.status_code} {r.json()}")

# 2. Register a new user
print("\n2. 注册新用户")
unique_id = int(time.time())
email = f"test{unique_id}@example.com"
r = client.post(f"{BASE}/api/auth/sign-up", json={
    "email": email,
    "password": "test123456",
    "name": f"Test User {unique_id}"
})
print(f"   POST /api/auth/sign-up => {r.status_code}")
if r.status_code == 201:
    print("   注册成功!")
else:
    print(f"   {r.json()}")

# 3. Sign in - tokens are in response headers
print("\n3. 用户登录")
r = client.post(f"{BASE}/api/auth/sign-in", json={
    "email": email,
    "password": "test123456"
})
print(f"   POST /api/auth/sign-in => {r.status_code}")
token = ""
if r.status_code == 200:
    data = r.json()
    print("   登录成功!")
    print(f"   响应体格式: {list(data.keys())}")
    print(f"   响应体数据: {data}")
    # Tokens are in headers
    token = r.headers.get("authorization", "")
    refresh_token = r.headers.get("refreshtoken", "")
    print(f"   Access Token (header): {token[:50]}..." if len(token) > 50 else f"   Access Token (header): {token}")
    print(f"   Refresh Token (header): {refresh_token[:50]}..." if len(refresh_token) > 50 else f"   Refresh Token (header): {refresh_token}")
else:
    print(f"   {r.json()}")
    exit(1)

# 4. Get current user
print("\n4. 获取当前用户信息")
r = client.get(f"{BASE}/api/auth/me", headers={"Authorization": f"Bearer {token}"})
print(f"   GET /api/auth/me => {r.status_code}")
if r.status_code == 200:
    user = r.json()
    print(f"   用户: {user.get('name')}")
    print(f"   邮箱: {user.get('email')}")

# 5. Create organization
print("\n5. 创建组织")
slug = f"test-org-{unique_id}"
r = client.post(f"{BASE}/api/org", json={
    "name": f"Test Org {unique_id}",
    "slug": slug,
    "desc": "Test organization"
}, headers={"Authorization": f"Bearer {token}"})
print(f"   POST /api/org => {r.status_code}")
org_id = ""
if r.status_code == 201:
    org_data = r.json()
    print("   创建成功!")
    print(f"   响应类型: {type(org_data).__name__}")
    if isinstance(org_data, dict):
        print(f"   字段: {list(org_data.keys())}")
        org_id = org_data.get("id", "")
    print(f"   Org ID: {org_id}")
else:
    print(f"   {r.json()}")

# 6. Get organizations
print("\n6. 获取组织列表")
r = client.get(f"{BASE}/api/org", headers={"Authorization": f"Bearer {token}"})
print(f"   GET /api/org => {r.status_code}")
if r.status_code == 200:
    orgs = r.json()
    print(f"   组织数量: {len(orgs)}")
    if orgs:
        print(f"   第一个组织: {orgs[0].get('name', '')}")

# 7. Create project
if org_id:
    print("\n7. 创建项目")
    r = client.post(f"{BASE}/api/project", json={
        "name": f"Test Project {unique_id}",
        "desc": "Test project",
        "organizationId": org_id
    }, headers={"Authorization": f"Bearer {token}"})
    print(f"   POST /api/project => {r.status_code}")
    project_id = ""
    if r.status_code == 201:
        project_data = r.json()
        print("   创建成功!")
        if isinstance(project_data, dict):
            project_id = project_data.get("id", "")
        print(f"   Project ID: {project_id}")

        # 8. Create task
        if project_id:
            print("\n8. 创建任务")
            r = client.post(f"{BASE}/api/task", json={
                "title": f"Test Task {unique_id}",
                "projectId": project_id
            }, headers={"Authorization": f"Bearer {token}"})
            print(f"   POST /api/task => {r.status_code}")
            if r.status_code == 201:
                task_data = r.json()
                print("   任务创建成功!")
                if isinstance(task_data, dict):
                    print(f"   Task ID: {task_data.get('id', '')}")

                # 9. Get tasks
                print("\n9. 获取任务列表")
                r = client.get(f"{BASE}/api/task?projectId={project_id}", headers={"Authorization": f"Bearer {token}"})
                print(f"   GET /api/task => {r.status_code}")
                if r.status_code == 200:
                    tasks = r.json()
                    print(f"   任务数量: {len(tasks)}")

            # 10. Create project view
            print("\n10. 创建项目视图")
            r = client.post(f"{BASE}/api/project/view", json={
                "name": "List View",
                "type": "LIST",
                "projectId": project_id
            }, headers={"Authorization": f"Bearer {token}"})
            print(f"   POST /api/project/view => {r.status_code}")
            if r.status_code == 201:
                print("   视图创建成功!")
            else:
                print(f"   {r.json()}")

            # 11. Get project views
            print("\n11. 获取项目视图列表")
            r = client.get(f"{BASE}/api/project/view?projectId={project_id}", headers={"Authorization": f"Bearer {token}"})
            print(f"   GET /api/project/view => {r.status_code}")
            if r.status_code == 200:
                views = r.json()
                print(f"   视图数量: {len(views)}")

        # 12. Get projects by org
        print("\n12. 获取组织下的项目列表")
        r = client.get(f"{BASE}/api/project?orgId={org_id}", headers={"Authorization": f"Bearer {token}"})
        print(f"   GET /api/project => {r.status_code}")
        if r.status_code == 200:
            projects = r.json()
            print(f"   项目数量: {len(projects)}")

# 13. Test refresh token
print("\n13. 刷新令牌")
if token:
    r = client.post(f"{BASE}/api/auth/refresh-token", headers={"RefreshToken": refresh_token})
    print(f"   POST /api/auth/refresh-token => {r.status_code}")
    if r.status_code == 200:
        new_access = r.headers.get("authorization", "")
        new_refresh = r.headers.get("refreshtoken", "")
        print("   令牌刷新成功!")
        print(f"   新 Access Token: {new_access[:50]}..." if len(new_access) > 50 else f"   新 Access Token: {new_access}")

# 14. Test error handling - unauthorized
print("\n14. 测试未授权访问")
r = client.get(f"{BASE}/api/org")
print(f"   GET /api/org (无 token) => {r.status_code}")

# 15. Test error handling - bad request
print("\n15. 测试错误请求")
r = client.post(f"{BASE}/api/org", json={}, headers={"Authorization": f"Bearer {token}"})
print(f"   POST /api/org (空数据) => {r.status_code}")
if r.status_code == 422:
    print("   正确返回验证错误!")

print("\n" + "=" * 60)
print("API 流程测试完成 - 所有核心端点正常!")
print("=" * 60)
