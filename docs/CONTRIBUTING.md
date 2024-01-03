# 贡献

非常感谢您有兴趣为 Open Assistant Api 做出贡献。

要为此项目做出贡献请遵循 "[fork and pull request](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project)" 工作流程，不要直接向仓库提交代码。

您可以先从解决现有 Issues 开始。

## 代码规范

本项目使用 Ruff 和 Black 做代码检查和格式化。

建议在推送到存储库之前运行 `make lint` 检查代码格式，运行 `make format` 格式化代码。

## 技术栈

### 中间件

- MySQL
- Redis
- MinIO (或任何支持 S3 协议的 OSS)

### 开发语言

- Python 3.10

### 开发库

- [Celery](https://github.com/celery/celery)
- [FastAPI](https://github.com/tiangolo/fastapi)
- [SQLModel](https://github.com/tiangolo/sqlmodel)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
- [LangChain](https://github.com/langchain-ai/langchain)
- OpenAI

### 工具

- Poetry
- Docker
- Docker Compose

## 项目结构

```
/open-assistant-api/
├── app
│   ├── api                                     ----- api控制器目录
│   │   ├── v1                                  ----- api v1 版本
│   │   ├── deps.py                             ----- 依赖注入项
│   │   └── routes.py                           ----- 路由注册表
│   ├── core                                    ----- 核心功能模块
│   │   ├── doc_loaders                         ----- 文档加载器
│   │   ├── runner                              ----- runner运行要逻辑
│   │   └── tools                               ----- Tools 实现
│   ├── exceptions                              ----- 自定义异常类
│   ├── models                                  ----- db模型目录
│   ├── providers                               ----- 核心服务提供者
│   │   ├── middleware                          ----- 自定义中间件
│   │   ├── app_provider.py                     ----- 注册应用的全局事件、中间件等
│   │   ├── celery_app.py                       ----- 任务调度器
│   │   ├── database.py                         ----- 数据库连接
│   │   ├── handle_exception.py                 ----- 异常处理器
│   │   ├── logging_provider.py                 ----- 集成loguru日志系统
│   │   ├── pagination_provider.py              ----- 分页插件
│   │   ├── response.py                         ----- 定义http统一响应体
│   │   ├── route_provider.py                   ----- 注册路由文件routes/*
│   │   └── storage.py                          ----- 对象存储
│   ├── schemas                                 ----- 数据模型
│   ├── services                                ----- 业务逻辑层
│   ├── libs                                    ----- 工具库
│   │   └── util.py
│   └── tasks                                   ----- 任务
│       └── run_task.py
├── config                                      ----- 配置目录
│   ├── celery.py                               ----- 调度器配置
│   ├── config.py                               ----- app配置
│   ├── database.py                             ----- 数据库配置
│   ├── storage.py                              ----- 对象存储配置
│   ├── llm.py                                  ----- 大模型相关配置
│   └── logging.py                              ----- 日志配置
├── migrations                                  ----- 数据库迁移
├── main.py                                     ----- app/api启动入口
├── poetry.lock
├── pyproject.toml                              ----- 项目依赖管理
├── logs                                        ----- 日志目录
├── volumes                                     ----- docker数据卷
├── tests                                       ----- 测试目录
│   ├── e2e                                     ----- 端到端测试
│   └── unit                                    ----- 单元测试
├── docker                                      ----- docker镜像相关
├── docs                                        ----- 文档
└── worker.py                                   ----- 调度任务启动入口
```

## 本地运行

### 环境准备

开发环境:

- Python >= 3.10
- [Poetry](https://python-poetry.org/docs/#installation)

安装 poetry

```sh
curl -sSL https://install.python-poetry.org | python3 -

# 或者
pip install poetry
```

安装依赖:

```sh
poetry install --no-root
```

### 配置

创建配置文件

```sh
cp .env.example .env
```

配置 openai api_key 和 bing search key

```sh
# openai api_key
OPENAI_API_KEY=<openai_api_key>

# bing search key
BING_SUBSCRIPTION_KEY=<bing_subscription_key>
```

### 部署中间件 (mysql, redis, minio)

```sh
docker compose -f docker-compose.middleware.yml up -d
```

### 启动应用

#### 初始化数据库

首次启动和版本升级时需要运行以下命令数据库生成数据库表:

```sh
alembic upgrade head
```

#### 启动 API

```sh
python main.py
```

#### 启动调度器

```sh
celery -A worker.celery_app worker -c 1 --loglevel DEBUG
```

### 访问 API

Api Base URL: http://127.0.0.1:8086/api/v1

接口文档地址: http://127.0.0.1:8086/docs

## 代码格式

代码提交前请先运行以下命令检查代码规范。

#### 检查代码是否需要格式化

```sh
make lint
```

#### 格式化代码

```sh
make format
```

## 数据库迁移 (改变 DB Model 时使用)

#### 生成迁移脚本

```sh
alembic revision --autogenerate
```

#### 执行迁移脚本

```sh
alembic upgrade head
```

## 构建 docker 镜像

```sh
docker build -t open-assistant-api .
```

## 部署

```sh
docker compose up -d
```