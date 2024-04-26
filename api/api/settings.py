from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Optional, List
from .data_management import PositionData, PlantRowData


class GroupModel(BaseModel):
    name: Optional[str] = ""
    apikey: str


class Settings(BaseSettings):
    groups: List[GroupModel]

    task2_rows_solution: List[PlantRowData]
    task3_positions_solution: List[PositionData]
    task4_positions: List[PositionData]

    postgres_host: Optional[str] = "postgres"
    postgres_port: Optional[str] = "5432"
    postgres_db: Optional[str] = "fre"
    postgres_user: str
    postgres_passwd: str

    default_database: Optional[str] = "Postgre"

    disable_ws_endpoint: Optional[bool] = False
    disable_admin_endpoint: Optional[bool] = False

    admin_api_key: str

    @property
    def api_keys(self):
        keys = [group.apikey for group in self.groups]
        return keys

    @property
    def group_names(self):
        names = [group.name for group in self.groups]
        return names


settings = Settings()
