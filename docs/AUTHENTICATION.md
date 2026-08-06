# 鉴权模块学习说明

这一批迁移实现邮箱密码鉴权的最小完整闭环，刻意保留清晰的层次，后续可以按同一规律迁移其他业务。

## 请求链路

```text
HTTP 请求
  → api/routes/auth.py           路由/控制层
  → api/dependencies.py          依赖组装与当前用户认证
  → services/auth_service.py     业务规则
  → repositories/user_repository.py
  → MongoDB users collection
```

辅助模块：

```text
schemas/auth.py        API 输入输出 DTO
models/user.py         MongoDB 内部文档类型
core/security.py       Argon2 密码与 JWT
core/errors.py         可预期业务异常
core/middleware.py     全局 HTTP 安全响应头
db/mongodb.py          客户端生命周期和数据库依赖
```

## 为什么认证不是普通 Middleware

全局 Middleware 会经过每个请求，适合 CORS、安全响应头、日志和请求 ID。是否需要登录则由具体接口决定，因此 FastAPI 更适合使用依赖：

```python
@router.get("/me")
async def get_me(current_user: CurrentUser) -> UserResponse:
    return current_user
```

没有声明 `CurrentUser` 的注册、登录和健康检查仍是公开接口；声明它的接口会自动验证访问令牌并加载用户。后续项目、任务接口可以复用同一个依赖。

## 已实现接口

| 方法 | 路径 | 是否公开 | 作用 |
| --- | --- | --- | --- |
| POST | `/api/auth/sign-up` | 是 | 邮箱注册并使用 Argon2 保存密码摘要 |
| POST | `/api/auth/sign-in` | 是 | 验证密码并签发访问/刷新令牌 |
| POST | `/api/auth/refresh-token` | 是 | 验证刷新令牌并轮换令牌对 |
| GET | `/api/auth/me` | 否 | 通过访问令牌读取当前用户 |

相同接口也在规范化前缀 `/api/v1/auth/*` 下提供。`/api/auth/*` 是现有 Next.js 前端的临时兼容路径。

登录成功暂时继续通过 `Authorization`、`RefreshToken` 响应头返回原前端所需的裸令牌；`/me` 同时接受裸令牌和标准的 `Bearer <token>`。新客户端应优先使用 Bearer 格式。CORS 明确暴露这两个响应头，否则浏览器 JavaScript 无法读取。

## 安全决策

- 密码只存 Argon2 摘要，永不保存或返回明文。
- Access Token 和 Refresh Token 使用不同密钥、有效期和 `type` claim。
- JWT 的 `sub` 保存用户 ID；每次访问仍从 MongoDB 加载用户，已删除用户的令牌立即失效。
- Refresh Token 只交给刷新接口，不允许当作访问令牌使用。
- MongoDB 为 `users.email` 建立唯一索引，业务检查之外还有数据库约束。
- 返回标准 401/403/409 HTTP 状态，不延续旧后端“所有错误都返回 HTTP 200”的设计。

目前为兼容原前端，令牌仍保存在浏览器 localStorage。这容易受 XSS 影响。完成前端契约迁移后，应评估将 Refresh Token 改为 `HttpOnly + Secure + SameSite` Cookie。

## 如何运行测试

快速测试不需要数据库：

```powershell
cd backend
uv run pytest -q
```

真实 MongoDB 集成测试会创建随机邮箱用户并在结束时删除，需要先启动 Compose：

```powershell
$env:RUN_MONGODB_TESTS="1"
uv run pytest tests/test_auth_mongodb.py -q
Remove-Item Env:RUN_MONGODB_TESTS
```

测试使用 `app.dependency_overrides` 将真实 Repository 替换为内存 Fake。这正是依赖注入的价值：Service 和 Router 可以在不启动 MongoDB 时快速验证，Repository 再由单独的集成测试负责。

## 尚未包含

- Google/Firebase 登录
- 邮箱验证与重发邮件
- 忘记密码和重置密码邮件
- Refresh Token 撤销列表、设备会话和退出登录
- 登录限流、失败次数锁定和审计日志

这些功能依赖外部服务或更完整的安全策略，后续在邮箱密码闭环稳定后单独迁移。

