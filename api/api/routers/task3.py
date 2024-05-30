from fastapi import APIRouter, Depends
from typing import Annotated, List
from ..data_management import PositionData
from ..security.group_auth import GroupAuth
from ..database.database import Database, DatabaseError
from ..tools.exception_convert import database_error_to_http_exception
from ..tools.event_publisher import EventPublisher, EventType
from ..data_management.infomessage import InfoMessage, InfoMessageEnum

TASK_NAME = "task3"

group_auth = GroupAuth()
eventpublisher = EventPublisher()
database = Database()

router = APIRouter(
    tags=["Task3"]
)

tags_metadata = [
    {
        "name": "Task3",
        "description": "Mapping in a Grassland Area"
    }
]


@router.post(
    "/add-position",
    status_code=201
)
async def add_position(
    positiondata: PositionData,
    group: Annotated[bool, Depends(group_auth)]
) -> InfoMessage:
    """
    Add the position for detected weed.
    """
    try:
        database.task3_add_positions(group, [positiondata])
        await eventpublisher.send_task_event(group,
                                             TASK_NAME,
                                             EventType.add_data)
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return InfoMessage(msg=InfoMessageEnum.ok)


@router.post(
    "/add-final-positions",
    status_code=201
)
async def add_final_positions(
    positiondata: List[PositionData],
    group: Annotated[bool, Depends(group_auth)]
) -> InfoMessage:
    """
    Add the final positions for detected weed.
    """
    try:
        database.task3_add_positions(group, positiondata, True)
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
    The robot signalizes that it has started working on task 3.
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
    The robot signalizes that it has finished working on task 3.
    """
    try:
        database.stop_task(group, TASK_NAME)
        await eventpublisher.send_task_event(group,
                                             TASK_NAME,
                                             EventType.stop_task)
    except DatabaseError as e:
        database_error_to_http_exception(e)
    return InfoMessage(msg=InfoMessageEnum.ok)
