from fastapi import APIRouter, Depends
from typing import Annotated
from ..data_management import PlantRowData
from ..security.group_auth import GroupAuth
from ..database.database import Database, DatabaseError
from ..tools.exception_convert import database_error_to_http_exception
from ..tools.event_publisher import EventPublisher, EventType
from ..data_management.infomessage import InfoMessage, InfoMessageEnum

TASK_NAME = "task2"

database = Database()

eventpublisher = EventPublisher()

group_auth = GroupAuth()

add_row_sql = """INSERT INTO task2(group_name,row_count,plant_count)
    VALUES (%s,%s,%s)"""

router = APIRouter(
    tags=["Task2"]
)

tags_metadata = [
    {
        "name": "Task2",
        "description": "Object Detection and Counting in a Maize Field"
    }
]


@router.post(
    "/add-row",
    status_code=201
)
async def add_row(
    rowdata: PlantRowData,
    group: Annotated[str, Depends(group_auth)]
) -> InfoMessage:
    """
    Add the plant count for a given row.
    """
    try:
        database.task2_add_row(group, rowdata.row_number, rowdata.plant_count)
        await eventpublisher.send_task_event(group,
                                             TASK_NAME,
                                             EventType.add_data)
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return InfoMessage(msg=InfoMessageEnum.ok)


@router.post(
    "/start",
    status_code=201
)
async def start_task(
    group: Annotated[str, Depends(group_auth)]
) -> InfoMessage:
    """
    The robot signalizes that it has started working on task 2.
    """
    try:
        database.start_task(group, TASK_NAME)
        await eventpublisher.send_task_event(group,
                                             TASK_NAME,
                                             EventType.start_task)
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return InfoMessage(msg=InfoMessageEnum.ok)


@router.post(
    "/stop",
    status_code=201
)
async def stop_task(
    group: Annotated[str, Depends(group_auth)]
) -> InfoMessage:
    """
    The robot signalizes that it has finished working on task 2.
    """
    try:
        database.stop_task(group, TASK_NAME)
        await eventpublisher.send_task_event(group,
                                             TASK_NAME,
                                             EventType.stop_task)
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return InfoMessage(msg=InfoMessageEnum.ok)
