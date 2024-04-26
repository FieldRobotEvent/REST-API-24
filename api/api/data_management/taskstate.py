from pydantic import BaseModel, Field
from datetime import datetime


class TaskState(BaseModel):
    """Schema for plant row data."""

    class Config:
        validate_assignment = True

    group: str = Field(
        description="Name of the group."
    )
    running: bool = Field(
        description="Status of the task."
    )
    timestamp: datetime = Field(
        description="Timestamp in UTC."
    )
