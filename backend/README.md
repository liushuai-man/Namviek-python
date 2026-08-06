# Namviek FastAPI backend

这是 Namviek Python Rebuild Demo 的独立后端。

## 本地运行

先在仓库根目录启动 MongoDB：

```powershell
docker compose up -d mongodb mongodb-init
docker compose ps
```

开发连接地址为：

```text
mongodb://localhost:27017/namviek?replicaSet=rs0&directConnection=true
```

`mongodb-init` 是一次性初始化容器，成功退出是正常现象；`mongodb` 应保持运行并显示 healthy。

```powershell
uv sync
uv run fastapi dev app/main.py
```

启动后访问：

- API 文档：<http://127.0.0.1:8000/docs>
- 健康检查：<http://127.0.0.1:8000/api/v1/health>

## 鉴权接口

| 方法 | 路径 | 作用 |
| --- | --- | --- |
| POST | `/api/auth/sign-up` | 邮箱注册 |
| POST | `/api/auth/sign-in` | 登录并返回访问/刷新令牌 |
| POST | `/api/auth/refresh-token` | 轮换令牌 |
| GET | `/api/auth/me` | 读取当前登录用户 |

实现结构和学习说明见 [`docs/AUTHENTICATION.md`](../docs/AUTHENTICATION.md)。

## 运行检查

```powershell
uv run ruff check .
uv run mypy app
uv run pytest
```
