import logging
from contextvars import ContextVar
from typing import Callable

import redis
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import AsyncAdaptedQueuePool, QueuePool
from sqlalchemy.orm import sessionmaker, scoped_session

from config.config import settings
from config.database import db_settings, redis_settings

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())

# database
connect_args = {}
database_url = db_settings.database_url
engine = create_engine(
    database_url,
    connect_args=connect_args,
    poolclass=QueuePool,
    pool_size=db_settings.DB_POOL_SIZE,
    pool_recycle=db_settings.DB_POOL_RECYCLE,
    echo=settings.DEBUG,
)
session = scoped_session(sessionmaker(bind=engine))

async_database_url = db_settings.async_database_url
async_engine = create_async_engine(
    async_database_url,
    connect_args=connect_args,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=db_settings.DB_POOL_SIZE,
    pool_recycle=db_settings.DB_POOL_RECYCLE,
    echo=settings.DEBUG,
)

# 创建session元类
async_session_local: Callable[..., AsyncSession] = sessionmaker(
    class_=AsyncSession,
    bind=async_engine,
)


def create_db_and_tables():
    logging.debug("Creating database and tables")
    import app.models  # noqa

    SQLModel.metadata.create_all(async_engine)
    logging.debug("Database and tables created successfully")


# redis
redis_pool = redis.ConnectionPool(
    host=redis_settings.REDIS_HOST,
    port=redis_settings.REDIS_PORT,
    db=redis_settings.REDIS_DB,
    password=redis_settings.REDIS_PASSWORD,
    decode_responses=True,
)
redis_client = redis.Redis(connection_pool=redis_pool)
