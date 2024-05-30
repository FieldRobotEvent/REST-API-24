from ..database import Database
from typing import List
from ...data_management.plantrow import PlantRowData
from ...data_management.positiondata import PositionData
from ...data_management.taskstate import TaskState


class DummyDB(Database):
    def __init__(self):
        super().__init__()

    def task2_add_rows(
            self,
            group: str,
            rows: List[PlantRowData],
            final: bool = False
            ) -> None:
        del group, rows, final

    def task2_get_rows(
            self,
            group: str,
            final: bool = False
            ) -> List[PlantRowData]:
        del group, final
        return []

    def task2_get_results(self, tz: str) -> List:
        del tz
        return []

    def task3_add_positions(
            self,
            group: str,
            positions: List[PositionData],
            final: bool = False
            ) -> None:
        del group, positions, final

    def task3_get_positions(
            self,
            group: str,
            final: bool = False
            ) -> List[PositionData]:
        del group, final

    def task3_get_results(self, tz: str) -> List:
        del tz
        return []

    def start_task(self, group: str, task: str) -> None:
        del group, task

    def stop_task(self, group: str, task: str) -> None:
        del group, task

    def get_start_stop(self, group: str, task: str) -> List[TaskState]:
        del group, task
        return []

    def clear_data(self, group: str, task: str) -> None:
        del group, task

    def reset_task(self, task: str) -> None:
        del task
