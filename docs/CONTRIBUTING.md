# Contribution

Thank you very much for your interest in contributing to Open Assistant Api.

To contribute to this project, please follow
the "[fork and pull request](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project)"
workflow, do not directly submit code to the repository.

You can start by solving existing Issues.

## Code Specification

This project uses Ruff and Black for code checking and formatting.

It is recommended to run `make lint` to check the code format before pushing to the repository, and run `make format` to
format the code.

## Technology Stack

### Middleware

- MySQL
- Redis
- MinIO (or any OSS that supports the S3 protocol)

### Development Language

- Python 3.10

### Development Libraries

- [Celery](https://github.com/celery/celery)
- [FastAPI](https://github.com/tiangolo/fastapi)
- [SQLModel](https://github.com/tiangolo/sqlmodel)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
- [LangChain](https://github.com/langchain-ai/langchain)
- OpenAI

### Tools

- Poetry
- Docker
- Docker Compose

## Project Structure

```
/open-assistant-api/
├── app
│   ├── api                                     ----- API controller directory
│   │   ├── v1                                  ----- API v1 version
│   │   ├── deps.py                             ----- Dependency injection items
│   │   └── routes.py                           ----- Route registry
│   ├── core                                    ----- Core function module
│   │   ├── doc_loaders                         ----- Document loaders
│   │   ├── runner                              ----- Runner operation logic
│   │   └── tools                               ----- Tools implementation
│   ├── exceptions                              ----- Custom exception classes
│   ├── models                                  ----- DB model directory
│   ├── providers                               ----- Core service providers
│   │   ├── middleware                          ----- Custom middleware
│   │   ├── app_provider.py                     ----- Register application's global events, middleware, etc.
│   │   ├── celery_app.py                       ----- Task scheduler
│   │   ├── database.py                         ----- Database connection
│   │   ├── handle_exception.py                 ----- Exception handler
│   │   ├── logging_provider.py                 ----- Integrated loguru logging system
│   │   ├── pagination_provider.py              ----- Pagination plugin
│   │   ├── response.py                         ----- Define HTTP unified response body
│   │   ├── route_provider.py                   ----- Register route files routes/*
│   │   └── storage.py                          ----- Object storage
│   ├── schemas                                 ----- Data models
│   ├── services                                ----- Business logic layer
│   ├── libs                                    ----- Utility library
│   │   └── util.py
│   └── tasks                                   ----- Tasks
│       └── run_task.py
├── config                                      ----- Configuration directory
│   ├── celery.py                               ----- Scheduler configuration
│   ├── config.py                               ----- App configuration
│   ├── database.py                             ----- Database configuration
│   ├── storage.py                              ----- Object storage configuration
│   ├── llm.py                                  ----- Large model related configuration
│   └── logging.py                              ----- Logging configuration
├── migrations                                  ----- Database migrations
├── main.py                                     ----- App/API startup entry
├── poetry.lock
├── pyproject.toml                              ----- Project dependency management
├── logs                                        ----- Log directory
├── volumes                                     ----- Docker data volumes
├── tests                                       ----- Test directory
│   ├── e2e                                     ----- End-to-end tests
│   └── unit                                    ----- Unit tests
├── docker                                      ----- Docker image related
├── docs                                        ----- Documentation
└── worker.py                                   ----- Task scheduling startup entry
```

## Local Running

### Environment Preparation

Development environment:

- Python >= 3.10
- [Poetry](https://python-poetry.org/docs/#installation)

Install poetry

```sh
curl -sSL https://install.python-poetry.org | python3 -

# or
pip install poetry
```

Install dependencies:

```sh
poetry install --no-root
```

### Configuration

Create configuration file

```sh
cp .env.example .env
```

Configure openai api_key and bing search key

```sh
# openai api_key
OPENAI_API_KEY=<openai_api_key>

# bing search key
BING_SUBSCRIPTION_KEY=<bing_subscription_key>
```

### Deploy Middleware (mysql, redis, minio)

```sh
docker compose -f docker-compose.middleware.yml up -d
```

### Start Application

#### Initialize Database

The following command needs to be run to generate the database table when first starting and upgrading the version:

```sh
alembic upgrade head
```

#### Start API

```sh
python main.py
```

#### Start Scheduler

```sh
celery -A worker.celery_app worker -c 1 --loglevel DEBUG
```

### Access API

Api Base URL: http://127.0.0.1:8086/api/v1

Interface documentation address: http://127.0.0.1:8086/docs

## Code Format

Please run the following command to check the code specification before submitting the code.

#### Check if the code needs to be formatted

```sh
make lint
```

#### Format Code

```sh
make format
```

## Database Migration (Use when changing DB Model)

#### Generate Migration Script

```sh
alembic revision --autogenerate
```

#### Execute Migration Script

```sh
alembic upgrade head
```

## Build Docker Image

```sh
docker build -t open-assistant-api .
```

## Deployment

```sh
docker compose up -d
```