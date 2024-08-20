from urllib.parse import quote_plus as urlquote

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    """mysql db"""

    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_DATABASE: str = "open_assistant"
    DB_USER: str = "root"
    DB_PASSWORD: str = "123456"
    DB_POOL_SIZE: int = 20
    DB_POOL_RECYCLE: int = 3600

    @property
    def database_url(self):
        return f"mysql+pymysql://{self.DB_USER}:{urlquote(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

    @property
    def async_database_url(self):
        return f"mysql+aiomysql://{self.DB_USER}:{urlquote(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

    class Config:
        env_file = ".env"


class RedisSettings(BaseSettings):
    """redis"""

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = None

    class Config:
        env_file = ".env"


db_settings = Settings()
redis_settings = RedisSettings()
