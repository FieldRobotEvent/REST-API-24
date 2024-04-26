from ..database import Database, DatabaseError
import psycopg2 as pg
from typing import List
from ...data_management.plantrow import PlantRowData
from ...data_management.positiondata import PositionData
from ...data_management.taskstate import TaskState


add_row_sql = """INSERT INTO task2(group_name,row_count,plant_count)
    VALUES (%s,%s,%s)"""

get_rows_sql = """SELECT row_count, plant_count FROM task2
    WHERE group_name = %s"""

add_position_sql = """INSERT INTO task3(group_name,x,y)
    VALUES (%s,%s,%s)"""

set_timer_sql = """INSERT INTO timer(group_name,task_name,running)
    VALUES (%s,%s,%s)"""

get_positions_sql = """SELECT x, y FROM task3
    WHERE group_name = %s"""

get_start_stop_sql = """ SELECT group_name, running, timestamp FROM timer
    WHERE group_name = %s
    AND task_name = %s
    ORDER BY timestamp DESC"""


class Postgres(Database):
    def __init__(self, database, host, user, password, port) -> None:
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.__connect()
        super().__init__()

    def __connect(self):
        self.conn = pg.connect(
            database=self.database,
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port
        )

    def task2_add_row(self, group: str, row: int, count: int) -> None:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        add_row_sql,
                        (group, row, count)
                    )
        except pg.Error as e:
            raise DatabaseError(
                backend_name=self.__class__.__name__,
                message=e.pgerror
            )

    def task2_get_rows(self, group: str) -> List[PlantRowData]:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        get_rows_sql,
                        (group,)
                    )
                    result = cursor.fetchall()
                    return [PlantRowData(row_number=r[0], plant_count=r[1])
                            for r in result]
        except pg.Error as e:
            raise DatabaseError(
                backend_name=self.__class__.__name__,
                message=e.pgerror
            )

    def task3_add_position(self, group: str, x: float, y: float) -> None:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        add_position_sql,
                        (group, x, y)
                    )
        except pg.Error as e:
            raise DatabaseError(
                backend_name=self.__class__.__name__,
                message=e.pgerror
            )

    def task3_get_positions(self, group: str) -> List[PositionData]:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        get_positions_sql,
                        (group,)
                    )
                    result = cursor.fetchall()
                    return [PositionData(x=r[0], y=r[1]) for r in result]
        except pg.Error as e:
            raise DatabaseError(
                backend_name=self.__class__.__name__,
                message=e.pgerror
            )

    def start_task(self, group: str, task: str) -> None:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        set_timer_sql,
                        (group, task, True)
                    )
        except pg.Error as e:
            raise DatabaseError(
                backend_name=self.__class__.__name__,
                message=e.pgerror
            )

    def stop_task(self, group: str, task: str) -> None:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        set_timer_sql,
                        (group, task, False)
                    )
        except pg.Error as e:
            raise DatabaseError(
                backend_name=self.__class__.__name__,
                message=e.pgerror
            )

    def get_start_stop(self, group: str, task: str) -> List[TaskState]:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        get_start_stop_sql,
                        (group, task)
                    )
                    result = cursor.fetchall()
                    return [TaskState(group=r[0], running=r[1], timestamp=r[2])
                            for r in result]
        except pg.Error as e:
            raise DatabaseError(
                backend_name=self.__class__.__name__,
                message=e.pgerror
            )
