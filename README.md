# Namviek Python Rebuild Demo

> [!IMPORTANT]
> 这是一个用于学习 Python 后端开发的非官方重构 Demo，不是原创项目，也不是 Namviek 官方发行版。

本项目基于开源项目 [hudy9x/namviek](https://github.com/hudy9x/namviek) 改造。Namviek 原有设计和代码成果归原作者及贡献者所有，感谢他们开放源代码供社区学习。本仓库保留 [GNU GPL v3.0](./LICENSE)，修改版本不会冒充上游官方版本。

## 项目目标

- 保留 Namviek 的 Next.js 前端，移除旧 Node.js 后端。
- 使用 Python、FastAPI 和 MongoDB 渐进式重写 API。
- 前后端只通过 HTTP、JSON 和 OpenAPI 契约交互。
- 在真实重构中学习 Python、异步编程、MongoDB 和自动化测试。

## 当前结构

```text
namviek-python/
├── frontend/              # 独立 Next.js 前端
│   ├── app/               # App Router 页面与功能
│   ├── packages/          # 前端仍在使用的上游共享代码
│   ├── public/            # 静态资源
│   ├── package.json       # 前端依赖和命令
│   └── yarn.lock          # 前端依赖锁文件
├── backend/               # 独立 FastAPI 后端
│   ├── app/               # Python 应用代码
│   ├── tests/             # Python 自动化测试
│   ├── pyproject.toml     # Python 依赖和工具配置
│   └── uv.lock            # Python 依赖锁文件
├── docs/
│   └── PROJECT_STRUCTURE.md
├── LICENSE
└── README.md
```

完整文件职责见 [项目结构说明](./docs/PROJECT_STRUCTURE.md)。旧 Node.js 后端保存在远程 Git 的 `backend/node` 分支中，主分支不再保留重复实现。

## 本地运行

先启动 MongoDB：

```powershell
docker compose up -d mongodb mongodb-init
docker compose ps
```

后端：

```powershell
cd backend
uv sync
uv run fastapi dev app/main.py
```

前端：

```powershell
cd frontend
yarn install
yarn dev
```

- 前端：<http://localhost:3000>
- 后端健康检查：<http://localhost:8000/api/v1/health>
- OpenAPI 文档：<http://localhost:8000/docs>

## 重构任务清单

### 1. 工程基线

- [x] 标注上游项目、原作者和非官方 Demo 身份
- [x] 保存旧 Node.js 实现到 `backend/node` 分支
- [x] 拆分独立的 `frontend/` 与 `backend/`
- [x] 移除 Nx、旧 Node 后端和旧部署配置
- [x] 初始化 FastAPI、Ruff、mypy 和 pytest
- [x] 实现 `/api/v1/health`
- [ ] 清理前端只在旧 Node 后端使用的 npm 依赖
- [ ] 用 API DTO 替换前端对 `@prisma/client` 类型的依赖

### 2. MongoDB

- [x] 使用 Docker Compose 启动本地 MongoDB replica set
- [x] 用 PyMongo `AsyncMongoClient` 管理连接生命周期
- [x] 配置环境变量、启动检查和连接关闭
- [ ] 学习 document、collection、ObjectId 和 BSON 类型
- [x] 为用户邮箱建立唯一索引
- [x] 编写第一条 MongoDB 鉴权集成测试和测试数据夹具
- [ ] 整理旧 Prisma schema 到 Python/MongoDB 模型的映射

### 3. API 迁移

- [x] 鉴权基础：邮箱注册、登录、刷新令牌和当前用户
- [x] 鉴权依赖、Argon2 密码摘要、JWT 与统一异常
- [ ] 鉴权扩展：邮箱验证、忘记/重置密码和 Google 登录
- [ ] 会话安全：退出登录、Refresh Token 撤销和登录限流
- [ ] 用户与个人资料
- [ ] 组织、邀请、成员和权限
- [ ] 项目、视图、状态和自定义字段
- [ ] 任务、负责人、标签、检查清单和排序
- [ ] 评论、活动记录、收藏和通知
- [ ] 文件存储、自动化、定时任务和报表

每个模块都应完成 Pydantic schema、业务实现、自动化测试、OpenAPI 契约和前端联调。

### 4. 前端契约与测试

- [ ] 从 FastAPI OpenAPI 文档生成 TypeScript API 类型
- [ ] 移除全部 Prisma Client 前端类型
- [ ] 为主要组件补充单元测试
- [ ] 重新建立 Playwright 或 Cypress E2E 工程
- [ ] 覆盖登录、创建组织、创建项目和任务等主要用户流程

原 `frontend-e2e` 只有 Nx/Cypress 示例骨架，已从主分支移除。正式 E2E 会在 API 基本稳定后重建，避免维护无效测试配置。

### 5. 构建与部署

- [ ] 创建前端、API 和后台任务生产镜像
- [ ] 编写开发与生产 Compose 配置
- [ ] 配置 MongoDB 数据卷、备份和恢复
- [ ] 配置密钥、HTTPS、反向代理和 CORS 白名单
- [ ] 添加 CI：格式检查、类型检查、测试和镜像构建
- [ ] 编写部署、升级、回滚和故障排查文档

## 学习节奏

每次只迁移一个小功能：阅读旧接口 → 定义 Pydantic 模型 → 实现 FastAPI 路由与 MongoDB 操作 → 编写测试 → 前端联调。这样每一步都有可运行结果，也能明确学到的 Python 知识。
