from fastapi import FastAPI
from .routers import task2, task3, task4, health, admin, websockets
from .settings import settings

all_tags_metadata = [
    *task2.tags_metadata,
    *task3.tags_metadata,
    *task4.tags_metadata,
    *health.tags_metadata
]

api_v2 = FastAPI(
    title="Field Robot Event 2024 - API",
    version="2",
    openapi_tags=all_tags_metadata
)

api_v2.include_router(task2.router, prefix="/task2")
api_v2.include_router(task3.router, prefix="/task3")
api_v2.include_router(task4.router, prefix="/task4")
api_v2.include_router(health.router, prefix="/health")

if not settings.disable_admin_endpoint:
    all_tags_metadata.append(*admin.tags_metadata)
    api_v2.include_router(admin.router, prefix="/admin")

if not settings.disable_ws_endpoint:
    api_v2.include_router(websockets.router, prefix="/ws")
