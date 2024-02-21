import logging

from fastapi import FastAPI
from app.providers import (
    logging_provider,
    app_provider,
    handle_exception,
    pagination_provider,
    route_provider,
    auth_provider,
)
from config.config import settings
import uvicorn


def create_app() -> FastAPI:
    _app = FastAPI()

    register(_app, logging_provider)
    register(_app, app_provider)
    register(_app, handle_exception)
    register(_app, pagination_provider)
    register(_app, auth_provider)

    boot(_app, route_provider)

    return _app


def register(_app, provider):
    provider.register(_app)
    logging.info(provider.__name__ + " registered")


def boot(_app, provider):
    provider.boot(_app)
    logging.info(provider.__name__ + " booted")


app = create_app()


@app.get("/")
async def root():
    return "Welcome to Open Assistant Api"


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        workers=settings.SERVER_WORKERS,
        reload=settings.ENV == "local",
    )
