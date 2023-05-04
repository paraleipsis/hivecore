from typing import Dict, Mapping, Union

from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_json(message: Union[Dict, Mapping], websocket: WebSocket):
        await websocket.send_json(message)

    @staticmethod
    async def send_str(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    @staticmethod
    async def send_bytes(message: bytes, websocket: WebSocket):
        await websocket.send_bytes(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
