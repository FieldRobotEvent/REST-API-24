from fastapi import FastAPI
from contextlib import asynccontextmanager
from .settings import settings
from .routers import task2, task3, task4, admin, websockets
from .v2 import api_v2
from .database.database_factory import DatabaseFactory
from .tools.websocket_handler import WebsocketHandler


@asynccontextmanager
async def lifespan(_: FastAPI):
    task2.group_auth.valid_groups = settings.groups
    task3.group_auth.valid_groups = settings.groups
    task4.positions = settings.task4_positions

    admin.api_key_auth.valid_key = settings.admin_api_key
    admin.task2_rows_solution = settings.task2_rows_solution
    admin.task3_positions_solution = settings.task3_positions_solution
    admin.groups = settings.group_names

    websockets.api_key_auth_ws.valid_key = settings.admin_api_key

    DatabaseFactory.initialise_databases(
        postgre_database=settings.postgres_db,
        postgre_host=settings.postgres_host,
        postgre_user=settings.postgres_user,
        postgre_password=settings.postgres_passwd,
        postgre_port=settings.postgres_port

    )

    factory = DatabaseFactory()
    task2.database = factory.get_database(settings.default_database)
    task3.database = factory.get_database(settings.default_database)
    admin.database = factory.get_database(settings.default_database)

    eventsockets = WebsocketHandler()
    task2.eventpublisher.set_ws_handler(eventsockets)
    task3.eventpublisher.set_ws_handler(eventsockets)
    websockets.eventsockets = eventsockets
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/fre2024", api_v2)
