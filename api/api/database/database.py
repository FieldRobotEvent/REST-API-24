from abc import ABC
from typing import List


class Database(ABC):
    def task2_add_row(self, group: str, row: int, count: int) -> None:
        del group, row, count
        raise NotImplementedError

    def task2_get_rows(self, group: str) -> List:
        del group
        raise NotImplementedError

    def task3_add_position(self, group: str, x: float, y: float) -> None:
        del group, x, y
        raise NotImplementedError

    def task3_get_positions(self, group: str) -> List:
        del group
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


class DatabaseError(Exception):
    def __init__(self, backend_name: str = "", message: str = "") -> None:
        self.message = message or 'unkown'
        self.backend_name = backend_name or 'unknown'
        super().__init__(self.message)
