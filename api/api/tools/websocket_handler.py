from fastapi import WebSocket, WebSocketDisconnect


class WebsocketHandler():
    def __init__(self) -> None:
        self.sockets = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.sockets.append(ws)
        await self.handle(ws)

    async def handle(self, ws: WebSocket):
        try:
            while True:
                await ws.receive_bytes()
        except WebSocketDisconnect:
            self._remove_ws(ws)

    def _remove_ws(self, ws: WebSocket):
        if ws in self.sockets:
            self.sockets.remove(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.sockets:
            ws.close()

    async def broadcast_json(self, json_string: str):
        for ws in self.sockets:
            await ws.send_json(json_string)
