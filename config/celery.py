from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    """celery"""

    CELERY_BROKER_URL: str = "redis://127.0.0.1:6379/1"

    class Config:
        env_file = ".env"


settings = Settings()
