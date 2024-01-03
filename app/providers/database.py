import logging
from contextvars import ContextVar

import redis
from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import QueuePool

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
    pool_recycle=3600,
    echo=True,
)


def create_db_and_tables():
    logging.debug("Creating database and tables")
    import app.models  # noqa

    SQLModel.metadata.create_all(engine)
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
