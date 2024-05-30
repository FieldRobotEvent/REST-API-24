from fastapi import APIRouter, WebSocket, Depends
from ..tools.websocket_handler import WebsocketHandler
from ..security.apikey_auth_ws import APIKeyAuthWS

eventsockets = WebsocketHandler()
api_key_auth_ws = APIKeyAuthWS()

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
    "/events/",
    dependencies=[Depends(api_key_auth_ws)]
)
async def add_websocket_subscriber(ws: WebSocket):
    await eventsockets.connect(ws)
