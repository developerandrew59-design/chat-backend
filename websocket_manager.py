import asyncio
import redis.asyncio as aioredis
import json
import logging

logger = logging.getLogger(__name__)

class ConnectionManager():
    def __init__(self):
        self.active_connections = {}
        self.redis = aioredis.from_url("redis://redis:6379")

    async def connect(self, websocket, room_id):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
        logger.info(f"WebSocket connected to room {room_id}. Total in room: {len(self.active_connections[room_id])}")

    async def disconnect(self, websocket, room_id):
        self.active_connections[room_id].remove(websocket)
        if len(self.active_connections[room_id]) == 0:
            del self.active_connections[room_id]
        logger.info(f"WebSocket disconnected from room {room_id}")

    async def broadcast(self, message, room_id):
        try:
            await self.redis.publish(f"room:{room_id}", message)
        except Exception as e:
            logger.error(f"Redis failed — falling back to direct broadcast. Error: {e}")
            if room_id in self.active_connections:
                for connection in self.active_connections[room_id]:
                    await connection.send_text(message)

    async def listen(self, room_id):
        try:
            pubsub = self.redis.pubsub()
            await pubsub.subscribe(f"room:{room_id}")
            async for msg in pubsub.listen():
                if msg["type"] == "message":
                    data = msg["data"].decode("utf-8")
                    if room_id in self.active_connections:
                        for connection in self.active_connections[room_id]:
                            await connection.send_text(data)
        except Exception as e:
            logger.error(f"Redis listener failed for room {room_id}. Error: {e}")

manager = ConnectionManager()               
    

         
       

