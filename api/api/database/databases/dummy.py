from ..database import Database
from typing import List
from ...data_management.plantrow import PlantRowData
from ...data_management.positiondata import PositionData
from ...data_management.taskstate import TaskState


class DummyDB(Database):
    def __init__(self):
        super().__init__()

    def task2_add_row(self, group: str, row: int, count: int) -> None:
        del group, row, count

    def task2_get_rows(self, group: str) -> List[PlantRowData]:
        del group
        return []

    def task3_add_position(self, group: str, x: float, y: float) -> None:
        del group, x, y

    def task3_get_positions(self, group: str) -> List[PositionData]:
        del group

    def start_task(self, group: str, task: str) -> None:
        del group, task

    def stop_task(self, group: str, task: str) -> None:
        del group, task

    def get_start_stop(self, group: str, task: str) -> List[TaskState]:
        del group, task
        return []
