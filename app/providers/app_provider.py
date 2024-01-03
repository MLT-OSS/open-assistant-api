import logging

from fastapi.middleware.cors import CORSMiddleware

from app.providers.middleware.http_process_time import HTTPProcessTimeMiddleware
from app.providers.middleware.unhandled_exception_handler import UnhandledExceptionHandlingMiddleware
from app.providers.database import redis_client
from config.config import settings


def register(app):
    app.debug = settings.DEBUG
    app.title = settings.NAME

    add_global_middleware(app)

    @app.on_event("startup")
    def startup():
        # create_db_and_tables()
        pass

    @app.on_event("shutdown")
    def shutdown():
        if redis_client:
            redis_client.close()

        logging.info("Application shutdown")


def add_global_middleware(app):
    app.add_middleware(UnhandledExceptionHandlingMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(HTTPProcessTimeMiddleware)
