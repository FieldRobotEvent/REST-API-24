from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from ..security.apikey_auth import APIKeyAuth
from ..database.database import Database, DatabaseError
from typing import List
from ..data_management.plantrow import PlantRowData
from ..data_management.positiondata import PositionData
from ..data_management.taskstate import TaskState
from ..data_management.infomessage import InfoMessage, InfoMessageEnum
from ..tools.exception_convert import database_error_to_http_exception
import pandas as pd
from tempfile import SpooledTemporaryFile
from enum import Enum
import zipfile as zf

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


class ResultTypeEnum(str, Enum):
    xlsx = 'xlsx'
    csv = 'csv'


def table_to_xlsx(file, table) -> SpooledTemporaryFile:
    with pd.ExcelWriter(file, date_format='YYYY-MM-DD HH:MM:SS') as writer:
        for group in groups:
            t = table.loc[table['group_name'] == group]
            t.to_excel(
                writer,
                index=False,
                float_format="%.3f",
                sheet_name=group)
    file.seek(0)
    return 'xlsx'


def table_to_zip(file, table) -> SpooledTemporaryFile:
    with zf.ZipFile(file, "w") as archive:
        for group in groups:
            t = table.loc[table['group_name'] == group]
            entry = t.to_csv(
                float_format="%.3f",
                date_format='%Y-%m-%d %H:%M:%S')
            index = group.lower().replace(" ", "_") + '.csv'
            archive.writestr(index, entry)
    file.seek(0)
    return 'zip'


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
    status_code=200,
    response_model_exclude_unset=True
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
    group: str,
    final: bool = False
) -> List[PlantRowData]:
    """
    Get a list of all uploaded plant counts for a given group:
    - ***group***: Name of the group
    """
    _check_group(group)
    try:
        result = database.task2_get_rows(group, final)
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return result


@router.get(
    "/task2/results",
    status_code=200
)
async def task2_get_result(
    tz: str = 'Europe/Berlin',
    filetype: ResultTypeEnum = ResultTypeEnum.xlsx,
    final: bool = True
):
    """
    Download results of task 2 as xlsx or zip of csv files.
    """
    try:
        table = (
            database
            .task3_get_results(tz)
            .query(f'final == {final}')
            .drop(['final'], axis=1)
            )
        file = SpooledTemporaryFile()
        match filetype:
            case ResultTypeEnum.xlsx:
                ending = table_to_xlsx(file, table)
            case ResultTypeEnum.csv:
                ending = table_to_zip(file, table)
            case _:
                ending = "error"
    except DatabaseError as e:
        database_error_to_http_exception(e)
    filename = "{task}{final}.{ending}".format(
        task='task2',
        final='_final' if final else '',
        ending=ending)
    return StreamingResponse(
        file,
        headers={
            'Content-Disposition': f"attachment; filename=\"{filename}\""
        }
    )


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


@router.post(
    "/task2/reset-group",
    status_code=200
)
async def task2_reset_group(
    group: str
) -> InfoMessage:
    """
    Clear all data for task2 for the given group
    as well as the start-stop signal:
    - ***group***: Name of the group
    """
    _check_group(group)
    try:
        database.clear_data(group, "task2")
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return InfoMessage(msg=InfoMessageEnum.ok)


@router.post(
    "/task2/reset",
    status_code=200
)
async def task2_reset() -> InfoMessage:
    """
    Clears all group data for task2
    """
    try:
        database.reset_task("task2")
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return InfoMessage(msg=InfoMessageEnum.ok)


@router.get(
    "/task3/positions-ground-truth",
    status_code=200,
    response_model_exclude_unset=True
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
    group: str,
    final: bool = False
) -> List[PositionData]:
    """
    Get a list of all uploaded weed positions by a given group:
    - ***group***: Name of the group
    """
    _check_group(group)
    try:
        result = database.task3_get_positions(group, final)
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return result


@router.get(
    "/task3/results",
    status_code=200
)
async def task3_get_result(
    tz: str = 'Europe/Berlin',
    filetype: ResultTypeEnum = ResultTypeEnum.xlsx,
    final: bool = True
):
    """
    Download results of task 3 as xlsx or zip of csv files.
    """
    try:
        table = (
            database
            .task3_get_results(tz)
            .query(f'final == {final}')
            .drop(['final'], axis=1)
            )
        file = SpooledTemporaryFile()
        match filetype:
            case ResultTypeEnum.xlsx:
                ending = table_to_xlsx(file, table)
            case ResultTypeEnum.csv:
                ending = table_to_zip(file, table)
            case _:
                ending = 'error'
    except DatabaseError as e:
        database_error_to_http_exception(e)
    filename = "{task}{final}.{ending}".format(
        task='task3',
        final='_final' if final else '',
        ending=ending)
    return StreamingResponse(
        file,
        headers={
            'Content-Disposition': f"attachment; filename=\"{filename}\""
        }
    )


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


@router.post(
    "/task3/reset",
    status_code=200
)
async def task3_reset() -> InfoMessage:
    """
    Clears all group data for task3
    """
    try:
        database.reset_task("task3")
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return InfoMessage(msg=InfoMessageEnum.ok)


@router.post(
    "/task3/reset-group",
    status_code=200
)
async def task3_reset_group(
    group: str
) -> InfoMessage:
    """
    Clear all data for task3 for the given group
    as well as the start-stop signal:
    - ***group***: Name of the group
    """
    _check_group(group)
    try:
        database.clear_data(group, "task3")
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return InfoMessage(msg=InfoMessageEnum.ok)
