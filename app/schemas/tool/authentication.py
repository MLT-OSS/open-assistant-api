import logging
from enum import Enum
from typing import Optional, Dict

from pydantic import BaseModel, Field, model_validator

from app.utils import aes_encrypt, aes_decrypt

logger = logging.getLogger(__name__)

__all__ = ["Authentication", "AuthenticationType"]


# This class utilizes code from the Open Source Project TaskingAI.
# The original code can be found at: https://github.com/TaskingAI/TaskingAI
class AuthenticationType(str, Enum):
    bearer = "bearer"
    basic = "basic"
    custom = "custom"
    none = "none"


# This function code from the Open Source Project TaskingAI.
# The original code can be found at: https://github.com/TaskingAI/TaskingAI
def validate_authentication_data(data: Dict):
    if not isinstance(data, dict):
        raise ValueError("Authentication should be a dict.")

    if "type" not in data or not data.get("type"):
        raise ValueError("Type is required for authentication.")

    if data["type"] == AuthenticationType.custom:
        if "content" not in data or data["content"] is None:
            raise ValueError("Content is required for custom authentication.")

    elif data["type"] == AuthenticationType.bearer:
        if "secret" not in data or data["secret"] is None:
            raise ValueError(f'Secret is required for {data["type"]} authentication.')

    elif data["type"] == AuthenticationType.basic:
        if "secret" not in data or data["secret"] is None:
            raise ValueError(f'Secret is required for {data["type"]} authentication.')
        # assume the secret is a base64 encoded string

    elif data["type"] == AuthenticationType.none:
        data["secret"] = None
        data["content"] = None

    return data


# This class utilizes code from the Open Source Project TaskingAI.
# The original code can be found at: https://github.com/TaskingAI/TaskingAI
class Authentication(BaseModel):
    encrypted: bool = Field(False)
    type: AuthenticationType = Field(...)
    secret: Optional[str] = Field(None, min_length=1, max_length=1024)
    content: Optional[Dict] = Field(None)

    @model_validator(mode="before")
    def validate_all_fields_at_the_same_time(cls, data: Dict):
        data = validate_authentication_data(data)
        return data

    def is_encrypted(self):
        return self.encrypted or self.type == AuthenticationType.none

    def encrypt(self):
        if self.encrypted or self.type == AuthenticationType.none:
            return
        if self.secret is not None:
            self.secret = aes_encrypt(self.secret)
        if self.content is not None:
            for key in self.content:
                self.content[key] = aes_encrypt(self.content[key])
        self.encrypted = True

    def decrypt(self):
        if not self.encrypted or self.type == AuthenticationType.none:
            return
        if self.secret is not None:
            self.secret = aes_decrypt(self.secret)
        if self.content is not None:
            for key in self.content:
                self.content[key] = aes_decrypt(self.content[key])
        self.encrypted = False
