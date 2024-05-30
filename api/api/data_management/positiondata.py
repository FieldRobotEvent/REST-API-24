from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PositionData(BaseModel):
    """Schema for position data. """

    class Config:
        validate_assignment = True
        json_schema_extra = {
            "example": {
                "x": 0.0,
                "y": 0.0
            }
        }

    x: float = Field(
        description="x coordinate. Unit is [metre]."
    )
    y: float = Field(
        description="y coordinate. Unit is [metre]."
    )
    timestamp: Optional[datetime] = Field(
        default=None,
        description="Admin only: Timestamp from database in UTC."
    )
