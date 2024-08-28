from contextlib import closing
from typing import Union, Generator

import boto3
from botocore.exceptions import ClientError

from app.exceptions.exception import ResourceNotFoundError
from config.storage import settings as s3_settings


class Storage:
    def __init__(self):
        self.bucket_name = None
        self.client = None

    def init(self):
        self.bucket_name = s3_settings.S3_BUCKET_NAME
        self.client = boto3.client(
            service_name="s3",
            aws_access_key_id=s3_settings.S3_ACCESS_KEY,
            aws_secret_access_key=s3_settings.S3_SECRET_KEY,
            endpoint_url=s3_settings.S3_ENDPOINT,
            region_name=s3_settings.S3_REGION,
        )

    def save(self, filename, data):
        self.client.put_object(Bucket=self.bucket_name, Key=filename, Body=data)

    def save_from_path(self, filename, local_file_path):
        self.client.upload_file(Filename=local_file_path, Bucket=self.bucket_name, Key=filename)

    def load(self, filename: str, stream: bool = False) -> Union[bytes, Generator]:
        if stream:
            return self.load_stream(filename)
        else:
            return self.load_once(filename)

    def load_once(self, filename: str) -> bytes:
        try:
            with closing(self.client) as client:
                data = client.get_object(Bucket=self.bucket_name, Key=filename)["Body"].read()
        except ClientError as ex:
            if ex.response["Error"]["Code"] == "NoSuchKey":
                raise ResourceNotFoundError("File not found")
            else:
                raise

        return data

    def load_stream(self, filename: str) -> Generator:
        def generate(filename: str = filename) -> Generator:
            try:
                with closing(self.client) as client:
                    response = client.get_object(Bucket=self.bucket_name, Key=filename)
                    for chunk in response["Body"].iter_chunks():
                        yield chunk
            except ClientError as ex:
                if ex.response["Error"]["Code"] == "NoSuchKey":
                    raise ResourceNotFoundError("File not found")
                else:
                    raise

        return generate()

    def download(self, filename, target_filepath):
        with closing(self.client) as client:
            client.download_file(self.bucket_name, filename, target_filepath)

    def exists(self, filename):
        with closing(self.client) as client:
            try:
                client.head_object(Bucket=self.bucket_name, Key=filename)
                return True
            except Exception:
                return False


storage = Storage()

storage.init()
