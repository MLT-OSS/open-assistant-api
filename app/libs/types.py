from datetime import datetime
from typing import Any

from pydantic_core import core_schema

from app.libs.util import datetime2timestamp

from app.libs.bson.objectid import ObjectId as ObjectId  # noqa


class Timestamp(datetime):
    @classmethod
    def __get_validators__(cls):
        yield datetime2timestamp

    @classmethod
    def __get_pydantic_core_schema__(
            cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(Timestamp),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.__get_validators__),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )
