# Namviek Python Rebuild Demo

> [!IMPORTANT]
> 这是一个用于学习 Python 后端开发的**非官方重构 Demo**，不是原创项目，也不是 Namviek 官方发行版。

本项目基于开源项目 [Namviek](https://github.com/hudy9x/namviek) 进行学习和改造。Namviek 及原有前端、后端代码的设计与实现成果归原项目作者及贡献者所有，感谢他们公开源代码，让学习者能够研究真实项目的工程实践。

本仓库的目标是保留 Namviek 前端的主要功能和 API 契约，逐步使用 **Python、FastAPI 和 MongoDB** 重写原 Node.js/Express 后端。它用于个人学习、技术实验和重构演示，不应被描述为独立原创产品。

## 上游项目与许可

- 上游项目：[hudy9x/namviek](https://github.com/hudy9x/namviek)
- 原项目作者：[hudy9x](https://github.com/hudy9x) 及 Namviek contributors
- 本仓库保留的许可证：[GNU General Public License v3.0](./LICENSE)
- 对上游代码所做的修改会在 Git 历史和本文档中标明

如果你分发本项目或修改后的版本，请同时遵守仓库内 `LICENSE` 的要求，并保留上游项目和作者信息。

## 重构目标

1. 将现有前端与后端解耦，使二者能够独立安装、开发、测试和部署。
2. 使用 FastAPI 重写 Express API，同时尽量保持前端 API 契约稳定。
3. 保留 MongoDB，在真实业务中学习文档建模、ObjectId、索引、聚合和事务。
4. 建立 Python 项目的类型检查、代码规范、自动化测试、数据库迁移和部署流程。
5. 以小步迁移的方式完成重构，确保每个阶段都有可以运行和验证的结果。

## 目标技术栈

| 领域 | 技术 |
| --- | --- |
| 前端 | Next.js、React、TypeScript、Tailwind CSS |
| Web API | Python 3.12+、FastAPI、Pydantic |
| 数据库 | MongoDB、PyMongo（异步 API） |
| 缓存与队列 | Redis，任务队列方案将在迁移调度功能时确定 |
| 测试 | pytest、pytest-asyncio、HTTPX |
| 质量工具 | Ruff、mypy |
| 环境与依赖 | uv |
| 构建部署 | Docker、Docker Compose |

## 目标目录结构

```text
namviek-python/
├── frontend/             # 从原项目整理出的 Next.js 前端
├── backend/              # 新 FastAPI 应用
│   ├── app/
│   │   ├── api/          # 路由层
│   │   ├── core/         # 配置、安全、异常处理
│   │   ├── db/           # MongoDB 连接、索引和数据访问
│   │   ├── models/       # 数据库存储模型
│   │   ├── schemas/      # API 输入输出模型
│   │   └── services/     # 业务逻辑
│   └── tests/
├── deploy/               # 容器及部署配置
└── docs/                 # 重构记录和学习笔记
```

目录迁移会分阶段进行。在新的 FastAPI 接口能够运行以前，原目录会暂时保留，避免一次性移动大量文件导致项目无法验证。

## 重构任务清单

### 阶段 0：建立安全基线

- [x] 标明项目是基于 Namviek 的非官方学习重构 Demo
- [x] 修改网页标题和项目包名
- [x] 保留许可证和上游作者信息
- [ ] 记录现有前端使用的 API、鉴权方式和响应格式
- [ ] 验证原前端可以独立构建

### 阶段 1：初始化 FastAPI 后端

- [ ] 创建 `backend` Python 工程和 `pyproject.toml`
- [ ] 配置开发、测试和生产环境变量
- [ ] 实现应用工厂、版本化路由和 `/health` 健康检查
- [ ] 配置统一响应、异常处理、日志和 CORS
- [ ] 配置 Ruff、mypy 和 pytest

### 阶段 2：学习并接入 MongoDB

- [ ] 使用 Docker Compose 启动 MongoDB replica set
- [ ] 使用 PyMongo 异步 API 管理连接生命周期
- [ ] 理解 database、collection、document 和 ObjectId
- [ ] 为核心查询设计唯一索引和复合索引
- [ ] 编写数据库测试和测试数据夹具
- [ ] 研究原 Prisma 模型并形成 Python/MongoDB 映射文档

### 阶段 3：按业务模块迁移 API

- [ ] 鉴权：注册、登录、刷新令牌、密码重置
- [ ] 用户与个人资料
- [ ] 组织、邀请、成员和权限
- [ ] 项目、视图、状态和自定义字段
- [ ] 任务、负责人、标签、检查清单和排序
- [ ] 评论、活动记录、收藏和通知
- [ ] 文件存储、自动化、定时任务和报表

每迁移一个模块，都要完成接口契约核对、单元测试、API 集成测试和前端联调，再移除对应的旧后端实现。

### 阶段 4：前后端彻底分离

- [ ] 将前端整理到独立目录和依赖清单
- [ ] 移除前端对旧 Nx 后端包的隐式依赖
- [ ] 通过环境变量配置 API 地址
- [ ] 生成并维护 OpenAPI 文档
- [ ] 完成主要用户流程的端到端测试
- [ ] 删除已经被替代的 Node.js 后端和无用构建配置

### 阶段 5：构建与部署

- [ ] 创建前端、API 和后台任务的生产镜像
- [ ] 编写生产用 Compose 配置和健康检查
- [ ] 配置 MongoDB 数据卷、备份与恢复方案
- [ ] 配置密钥、HTTPS、反向代理和 CORS 白名单
- [ ] 添加 CI：检查、测试和镜像构建
- [ ] 编写部署、升级、回滚和故障排查文档

## 学习方式

重构采用“小步闭环”：先阅读一个原接口，再设计 Pydantic schema，随后实现 FastAPI 路由和 MongoDB 操作，最后通过测试及前端联调验证。每一步都会说明相关 Python 知识，例如：

- 类型注解、数据类与 Pydantic 模型的区别
- `async`/`await` 与异步数据库访问
- FastAPI 依赖注入
- Python 模块、包和分层设计
- MongoDB 文档建模、索引、聚合管道和事务
- pytest fixture、mock 与集成测试

## 当前状态

项目刚进入重构准备阶段。现有 Node.js 后端暂时保留，仅作为行为参考；新的 FastAPI 后端将在下一阶段建立。在对应功能完成测试前，不会直接删除旧实现。

