from ..database import Database, DatabaseError
import pandas as pd
import psycopg2 as pg
from psycopg2 import sql
from typing import List
from ...data_management.plantrow import PlantRowData
from ...data_management.positiondata import PositionData
from ...data_management.taskstate import TaskState
import warnings
# Ignore SQLAlchemy Warning
warnings.simplefilter(action='ignore', category=UserWarning)


add_row_sql = """INSERT INTO task2(group_name,row_count,plant_count,final)
    VALUES (%s,%s,%s,%s)"""

get_rows_sql = """SELECT row_count, plant_count, timestamp FROM task2
    WHERE group_name = %s
    AND final = %s
    ORDER BY timestamp DESC"""

add_position_sql = """INSERT INTO task3(group_name,x,y,final)
    VALUES (%s,%s,%s,%s)"""

set_timer_sql = """INSERT INTO timer(group_name,task_name,running)
    VALUES (%s,%s,%s)"""

get_positions_sql = """SELECT x, y, timestamp FROM task3
    WHERE group_name = %s
    AND final = %s
    ORDER BY timestamp DESC"""

get_start_stop_sql = """ SELECT group_name, running, timestamp FROM timer
    WHERE group_name = %s
    AND task_name = %s
    ORDER BY timestamp DESC"""

delete_timer = """DELETE FROM timer
    WHERE task_name = %s
    AND group_name = %s
"""


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

    def task2_add_rows(
            self,
            group: str,
            rows: List[PlantRowData],
            final: bool = False
            ) -> None:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    for row in rows:
                        cursor.execute(
                            add_row_sql,
                            (group, row.row_number, row.plant_count, final)
                        )
        except pg.Error as e:
            raise DatabaseError(
                backend_name=self.__class__.__name__,
                message=e.pgerror
            )

    def task2_get_rows(
            self,
            group: str,
            final: bool = False
            ) -> List[PlantRowData]:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        get_rows_sql,
                        (group, final)
                    )
                    result = cursor.fetchall()
                    return [
                        PlantRowData(
                            row_number=r[0],
                            plant_count=r[1],
                            timestamp=r[2]
                        )
                        for r in result
                    ]
        except pg.Error as e:
            raise DatabaseError(
                backend_name=self.__class__.__name__,
                message=e.pgerror
            )

    def task2_get_results(self, tz: str) -> List:
        with self.conn as conn:
            table = pd.read_sql("""
                                SELECT
                                group_name,row_count,plant_count,timestamp,final
                                FROM task2
                                ORDER BY timestamp DESC""",
                                conn,
                                parse_dates={"timestamp": {"utc": True}})
            table['timestamp'] = table['timestamp'].dt.tz_convert(tz)
            table['timestamp'] = table['timestamp'].dt.tz_localize(None)
            return table

    def task3_add_positions(
            self,
            group: str,
            positions: List[PositionData],
            final: bool = False
            ) -> None:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    for pos in positions:
                        cursor.execute(
                            add_position_sql,
                            (group, pos.x, pos.y, final)
                        )
        except pg.Error as e:
            raise DatabaseError(
                backend_name=self.__class__.__name__,
                message=e.pgerror
            )

    def task3_get_positions(
            self,
            group: str,
            final: bool = False
            ) -> List[PositionData]:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        get_positions_sql,
                        (group, final)
                    )
                    result = cursor.fetchall()
                    return [
                        PositionData(x=r[0], y=r[1], timestamp=r[2])
                        for r in result
                    ]
        except pg.Error as e:
            raise DatabaseError(
                backend_name=self.__class__.__name__,
                message=e.pgerror
            )

    def task3_get_results(self, tz: str) -> List:
        with self.conn as conn:
            table = pd.read_sql("""
                                SELECT
                                group_name,x,y,timestamp,final
                                FROM task3
                                ORDER BY timestamp DESC""",
                                conn,
                                parse_dates={"timestamp": {"utc": True}})
            table['timestamp'] = table['timestamp'].dt.tz_convert(tz)
            table['timestamp'] = table['timestamp'].dt.tz_localize(None)
            return table

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
                    return [
                        TaskState(group=r[0], running=r[1], timestamp=r[2])
                        for r in result
                    ]
        except pg.Error as e:
            raise DatabaseError(
                backend_name=self.__class__.__name__,
                message=e.pgerror
            )

    def clear_data(self, group: str, task: str) -> None:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        sql.SQL(
                            "DELETE FROM {} WHERE group_name = %s"
                        ).format(sql.Identifier(task)),
                        (group,)
                    )
                    cursor.execute(
                        delete_timer,
                        (task, group)
                    )
        except pg.Error as e:
            print(e.__str__())
            raise DatabaseError(
                backend_name=self.__class__.__name__,
                message=e.pgerror
            )

    def reset_task(self, task: str) -> None:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        sql.SQL(
                            "DELETE FROM {}"
                        ).format(sql.Identifier(task))
                    )
                    cursor.execute(
                        """DELETE FROM timer WHERE task_name = %s""",
                        (task,)
                    )
        except pg.Error as e:
            print(e.__str__())
            raise DatabaseError(
                backend_name=self.__class__.__name__,
                message=e.pgerror
            )
