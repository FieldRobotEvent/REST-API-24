from pydantic import BaseModel, Field
from enum import Enum


class InfoMessageEnum(str, Enum):
    ok = 'ok'
    fail = 'fail'


class InfoMessage(BaseModel):
    """Schema for info message."""

    class Config:
        validate_assignment = True
        json_schema_extra = {
            "example": {
                "msg": "ok",
            }
        }

    msg: InfoMessageEnum = Field(
        description="ok on success. fail on failure"
    )
