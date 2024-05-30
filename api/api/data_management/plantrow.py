from pydantic import BaseModel, NonNegativeInt, PositiveInt, Field
from typing import Optional
from datetime import datetime


class PlantRowData(BaseModel):
    """Schema for plant row data."""

    class Config:
        validate_assignment = True
        json_schema_extra = {
            "example": {
                "row_number": 1,
                "plant_count": 0
            }
        }

    row_number: PositiveInt = Field(
        description="Number of the row starting at 1."
    )
    plant_count: NonNegativeInt = Field(
        description="Number of counted plants for the given row."
    )
    timestamp: Optional[datetime] = Field(
        default=None,
        description="Admin only: Timestamp from database in UTC."
    )
