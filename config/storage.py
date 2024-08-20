from pydantic.v1 import BaseSettings


class Settings(BaseSettings):

    """file service module"""

    FILE_SERVICE_MODULE = "app.services.file.impl.oss_file.OSSFileService"

    """aws s3 storage for oss file service"""
    S3_ENDPOINT: str = "http://minio:9000"
    S3_BUCKET_NAME: str = "open_assistant"
    S3_ACCESS_KEY: str = "ak-xxxx"
    S3_SECRET_KEY: str = "sk-xxxx"
    S3_REGION: str = "us-east-1"

    class Config:
        env_file = ".env"


settings = Settings()
