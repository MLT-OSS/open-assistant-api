import uuid
from datetime import datetime

import jwt


def datetime2timestamp(value: datetime):
    if not value:
        return None
    return value.timestamp()


def str2datetime(value: str):
    if not value:
        return None
    return datetime.fromisoformat(value)


def is_valid_datetime(date_str, format="%Y-%m-%d %H:%M:%S"):
    if not date_str or not isinstance(date_str, str):
        return False
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False


def random_uuid() -> str:
    return "ml-" + str(uuid.uuid4()).replace("-", "")


def verify_jwt_expiration(token):
    decoded_token = jwt.decode(token, options={"verify_signature": False, "verify_exp": False})
    expiration_time = datetime.fromtimestamp(decoded_token['exp'])
    current_time = datetime.now()
    return current_time < expiration_time
