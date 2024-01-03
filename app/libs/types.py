from datetime import datetime

from app.libs.util import datetime2timestamp

from app.libs.bson.objectid import ObjectId as ObjectId  # noqa


class Timestamp(datetime):
    @classmethod
    def __get_validators__(cls):
        yield datetime2timestamp
