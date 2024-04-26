from fastapi import APIRouter, WebSocket
from ..tools.websocket_handler import WebsocketHandler

eventsockets = WebsocketHandler()

router = APIRouter(
    tags=["Websockets"]
)

tags_metadata = [
    {
        "name": "Websockets",
        "description": "Websockets to monitor activity"
    }
]


@router.websocket(
    "/events"
)
async def add_websocket_subscriber(ws: WebSocket):
    await eventsockets.connect(ws)
