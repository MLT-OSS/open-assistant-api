import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    NAME: str = "open-assistant-api"
    DEBUG: bool = False
    ENV: str = "prod"

    BASE_PATH: str = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8086
    SERVER_WORKERS: int = 8
    API_PREFIX: str = "/api"

    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    TWILIO_WEBHOOK_BASE_URL: str = ""
    GOOGLE_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"
    DRAGON_GREETING_LANGUAGE: str = "de"
    DRAGON_COMPANY_NAME: str = "Dragon & Partner"

    AUTH_ENABLE: bool = False
    AUTH_ADMIN_TOKEN: str = "admin"
    AES_ENCRYPTION_KEY: str = "xxx"

    class Config:
        env_prefix = "APP_"
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
