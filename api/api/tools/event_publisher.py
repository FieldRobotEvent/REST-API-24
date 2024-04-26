import json
from enum import Enum
from ..tools.websocket_handler import WebsocketHandler


class EventType(str, Enum):
    add_data = "add_data"
    start_task = "start_task"
    stop_task = "stop_task"


class EventPublisher():
    def __init__(self) -> None:
        self.wshandler = None

    def set_ws_handler(self, handler: WebsocketHandler):
        self.wshandler = handler

    async def send_task_event(self, group: str, task: str, type: EventType):
        msg = {
            'group': group,
            'task': task,
            'event': type
        }
        json_str = json.dumps(msg)
        if self.wshandler:
            json_str = json.dumps(msg)
            await self.wshandler.broadcast_json(json_str)
