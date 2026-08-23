"""WebSocket connection manager for real-time updates."""

from typing import Dict, List
from fastapi import WebSocket
import structlog

logger = structlog.get_logger()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = []
        self.active_connections[channel].append(websocket)
        logger.info("WebSocket connected", channel=channel)

    def disconnect(self, websocket: WebSocket, channel: str):
        if channel in self.active_connections:
            self.active_connections[channel] = [
                ws for ws in self.active_connections[channel] if ws != websocket
            ]
        logger.info("WebSocket disconnected", channel=channel)

    async def broadcast(self, channel: str, message: dict):
        if channel in self.active_connections:
            for connection in self.active_connections[channel]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

    async def send_personal(self, websocket: WebSocket, message: dict):
        try:
            await websocket.send_json(message)
        except Exception:
            pass

manager = ConnectionManager()
