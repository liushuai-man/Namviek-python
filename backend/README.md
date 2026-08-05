# Namviek FastAPI backend

这是 Namviek Python Rebuild Demo 的独立后端。

## 本地运行

```powershell
uv sync
uv run fastapi dev app/main.py
```

启动后访问：

- API 文档：<http://127.0.0.1:8000/docs>
- 健康检查：<http://127.0.0.1:8000/api/v1/health>

## 运行检查

```powershell
uv run ruff check .
uv run mypy app
uv run pytest
```

