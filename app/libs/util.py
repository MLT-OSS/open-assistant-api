import uuid
from datetime import datetime


def datetime2timestamp(value: datetime):
    if not value:
        return None
    return value.timestamp()


def random_uuid() -> str:
    return "ml-" + str(uuid.uuid4()).replace("-", "")
