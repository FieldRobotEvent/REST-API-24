from fastapi import APIRouter, Depends
from ..security.apikey_auth import APIKeyAuth
from ..database.database import Database, DatabaseError
from fastapi import status, HTTPException
from typing import List
from ..data_management.plantrow import PlantRowData
from ..data_management.positiondata import PositionData
from ..data_management.taskstate import TaskState
from ..tools.exception_convert import database_error_to_http_exception

database = Database()

groups = []
task2_rows_solution = []
task3_positions_solution = []

api_key_auth = APIKeyAuth()

router = APIRouter(
    tags=["Admin"],
    dependencies=[Depends(api_key_auth)]
)

tags_metadata = [
    {
        "name": "Admin",
        "description": "Admin endpoint for FRE2024"
    }
]


def _check_group(group: str) -> None:
    if group not in groups:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Group {group} is unknown"
        )


@router.get(
    "/teams",
    status_code=200
)
async def get_teams() -> List[str]:
    """
    Get a list of all known groups.
    """
    return groups


@router.get(
    "/task2/count-ground-truth",
    status_code=200
)
async def task2_get_count_ground_truth() -> List[PlantRowData]:
    """
    Get the solution for task 2.
    """
    return task2_rows_solution


@router.get(
    "/task2/count",
    status_code=200
)
async def task2_get_count(
    group: str
) -> List[PlantRowData]:
    """
    Get a list of all uploaded plant counts for a given group:
    - ***group***: Name of the group
    """
    _check_group(group)
    try:
        result = database.task2_get_rows(group)
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return result


@router.get(
    "/task2/start-stop",
    status_code=200
)
async def task2_start_stop(
    group: str
) -> List[TaskState]:
    """
    Get all start and stop signals for task 2 in decending order
    by time for a given group:
    - ***group***: Name of the group
    """
    _check_group(group)
    try:
        result = database.get_start_stop(group, "task2")
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return result


@router.get(
    "/task3/positions-ground-truth",
    status_code=200
)
async def task3_get_positions_ground_truth(
) -> List[PositionData]:
    """
    Get the solution for task 3.
    """
    return task3_positions_solution


@router.get(
    "/task3/positions",
    status_code=200
)
async def task3_get_positions(
    group: str
) -> List[PositionData]:
    """
    Get a list of all uploaded weed positions by a given group:
    - ***group***: Name of the group
    """
    _check_group(group)
    try:
        result = database.task3_get_positions(group)
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return result


@router.get(
    "/task3/start-stop",
    status_code=200
)
async def task3_start_stop(
    group: str
) -> List[TaskState]:
    """
    Get all start and stop signals for task 3 in decending order
    by time for a given group:
    - ***group***: Name of the group
    """
    _check_group(group)
    try:
        result = database.get_start_stop(group, "task3")
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return result
