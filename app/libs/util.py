from datetime import datetime


def datetime2timestamp(value: datetime):
    if not value:
        return None
    return value.timestamp()
