from abc import ABC
from typing import List
from ..data_management.plantrow import PlantRowData
from ..data_management.positiondata import PositionData


class Database(ABC):
    def task2_add_rows(
            self,
            group: str,
            rows: List[PlantRowData],
            final: bool = False
            ) -> None:
        del group, rows, final
        raise NotImplementedError

    def task2_get_rows(self, group: str, final: bool = False) -> List:
        del group, final
        raise NotImplementedError

    def task2_get_results(self, tz: str) -> List:
        del tz
        raise NotImplementedError

    def task3_add_positions(
            self,
            group: str,
            positions: List[PositionData],
            final: bool = False
            ) -> None:
        del group, positions, final
        raise NotImplementedError

    def task3_get_positions(self, group: str, final: bool = False) -> List:
        del group, final
        raise NotImplementedError

    def task3_get_results(self, tz: str) -> List:
        del tz
        raise NotImplementedError

    def start_task(self, group: str, task: str) -> None:
        del group, task
        raise NotImplementedError

    def stop_task(self, group: str, task: str) -> None:
        del group, task
        raise NotImplementedError

    def get_start_stop(self, group: str, task: str) -> List:
        del group, task
        raise NotImplementedError

    def clear_data(self, group: str, task: str) -> None:
        del group, task
        raise NotImplementedError

    def reset_task(self, task: str) -> None:
        del task
        raise NotImplementedError


class DatabaseError(Exception):
    def __init__(self, backend_name: str = "", message: str = "") -> None:
        self.message = message or 'unkown'
        self.backend_name = backend_name or 'unknown'
        super().__init__(self.message)
