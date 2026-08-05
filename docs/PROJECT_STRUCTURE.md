# 项目结构与文件职责

本文说明主分支保留的目录和配置为什么存在。原则是：前后端独立管理依赖，只共享 API 契约，不共享数据库模型或运行时代码。

## 根目录

| 路径 | 作用 | 是否提交 |
| --- | --- | --- |
| `frontend/` | Next.js 浏览器应用，独立安装和构建 | 是 |
| `backend/` | FastAPI 服务，独立安装、测试和运行 | 是 |
| `docs/` | 架构、迁移和学习说明 | 是 |
| `compose.yaml` | 本地 MongoDB replica set 与持久化卷配置 | 是 |
| `.editorconfig` | 统一编辑器的换行、缩进等基础格式 | 是 |
| `.gitignore` | 排除依赖、缓存、密钥和构建产物 | 是 |
| `README.md` | 项目身份、快速开始和总任务清单 | 是 |
| `LICENSE` | 上游项目使用的 GPL v3.0 许可证 | 是 |

`.idea/`、`.venv/`、`node_modules/`、`.next/`、缓存、构建产物和真实 `.env` 都是本机生成内容，不应提交。

## `frontend/`

| 路径 | 作用 |
| --- | --- |
| `app/` | Next.js App Router 页面、布局以及页面相关功能 |
| `app/_components/` | 多个页面复用的应用级组件 |
| `app/_features/` | 按业务能力组织的前端功能，例如任务、项目和报表 |
| `app/_hooks/` | React 自定义 Hooks |
| `app/_events/` | 前端实时事件及状态同步逻辑 |
| `components/` | 根页面等较早期的共享组件；后续逐步归并到 `app/_components` |
| `layouts/` | 组织、用户和根布局组件 |
| `libs/` | Firebase 等浏览器端第三方集成封装 |
| `services/` | HTTP 请求层，是前端访问 FastAPI 的唯一入口 |
| `store/` | Zustand 等客户端状态管理 |
| `public/` | 图片、图标、Service Worker 和导入模板等静态资源 |
| `packages/auth-client/` | 上游认证 UI 与客户端会话逻辑，当前仍被前端使用 |
| `packages/core/` | 上游通用 TypeScript 工具与校验；后续只保留浏览器需要的部分 |
| `packages/ui-components/` | 上游共享 React UI 组件 |
| `.env.example` | 只包含可暴露给浏览器的 `NEXT_PUBLIC_*` 示例变量 |
| `package.json` | 前端 npm 依赖以及 `dev/build/start/typecheck` 命令 |
| `yarn.lock` | 锁定前端依赖的准确版本，应提交 |
| `next.config.js` | 独立 Next.js 构建配置，不再依赖 Nx |
| `tsconfig.json` | TypeScript 严格检查和前端路径别名 |
| `tailwind.config.js` | Tailwind CSS 扫描路径和主题配置 |
| `postcss.config.js` | Tailwind/PostCSS 构建配置 |
| `.prettierrc`、`.prettierignore` | 前端代码格式配置 |
| `next-env.d.ts`、`index.d.ts` | Next.js 和额外前端模块的类型声明 |
| `types/` | 已从旧数据库包解耦、但尚未由 OpenAPI 生成的前端临时 DTO |

### 前端遗留边界

部分前端源码仍从 `@prisma/client` 导入 `Task`、`User` 等类型。这只是原 TypeScript Monorepo 留下的临时兼容依赖，并不表示前端可以访问 MongoDB。迁移模块时，应使用 FastAPI OpenAPI 生成的 TypeScript DTO 替代这些类型，最终删除 Prisma Client。

`packages/` 暂时放在 `frontend/` 内，是因为它们只服务前端。待 API 迁移稳定后，可以继续将它们归并成普通的 `components/`、`lib/` 和 `types/`，进一步减少目录层级。

## `backend/`

| 路径 | 作用 |
| --- | --- |
| `app/__init__.py` | 明确 `app` 是 Python 包 |
| `app/main.py` | FastAPI 应用工厂和 ASGI 应用入口 |
| `app/api/router.py` | 汇总版本化 API 路由 |
| `app/api/routes/health.py` | HTTP 健康检查及其响应模型 |
| `tests/test_health.py` | 使用 TestClient 验证第一个 API 契约 |
| `pyproject.toml` | Python 版本、运行依赖、开发依赖以及工具配置 |
| `uv.lock` | uv 生成的跨平台依赖锁文件，应提交 |
| `.env.example` | 后端配置示例，不包含真实密钥 |
| `README.md` | 后端独立运行和检查命令 |

后续按需要增加：

```text
backend/app/
├── api/          # HTTP 路由与依赖
├── core/         # 配置、安全、日志和异常
├── db/           # MongoDB 客户端、索引和仓储
├── models/       # MongoDB 内部文档模型
├── schemas/      # 对外 API 的 Pydantic 模型
└── services/     # 与 HTTP、数据库框架无关的业务逻辑
```

## 已移除内容

| 原路径 | 移除原因 | 如何找回 |
| --- | --- | --- |
| `apps/backend/` | 旧 Express 后端，主分支由 FastAPI 替代 | `backend/node` 分支 |
| `apps/frontend-e2e/` | 只有旧 Nx/Cypress 示例，API 稳定后重建 | `backend/node` 分支 |
| `packages/database/` | Prisma/Node 数据访问层，不属于 Python 后端 | `backend/node` 分支 |
| `packages/event-bus/` | Node 事件总线，后续按真实需求用 Python 重写 | `backend/node` 分支 |
| `packages/task-runner*` | Node 调度器及测试，后续用 Python 任务方案重写 | `backend/node` 分支 |
| `nx.json`、`project.json` | 不再使用 Nx 编排前后端 | `backend/node` 分支 |
| `fly*.toml`、`render.yaml`、`netlify.toml` | 上游部署配置与重构后的架构不匹配 | `backend/node` 分支 |
| `docker/`、旧 Compose | 面向旧 Node 后端，后续重新编写 | `backend/node` 分支 |
| `CONTRIBUTING.md`、`DOCUMENTS.md`、`SECURITY.md` | 上游流程文档不适用于个人重构 Demo | `backend/node` 分支 |
