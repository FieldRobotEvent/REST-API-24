from fastapi import APIRouter, HTTPException, status
from ..data_management import PositionData
from typing import List

positions = None

router = APIRouter(
    tags=["Task4"]
)
tags_metadata = [
    {
        "name": "Task4",
        "description": "Application in a Grassland Area"
    }
]


@router.get(
    "/get-positions",
    response_model_exclude_unset=True
)
async def get_positions() -> List[PositionData]:
    """
    Get the weed locations for task 4.
    """
    if not positions:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Positions are not initialized"
        )
    return positions
