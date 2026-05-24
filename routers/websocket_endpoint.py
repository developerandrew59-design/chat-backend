from fastapi import APIRouter,WebSocket,WebSocketDisconnect
from websocket_manager import manager

router=APIRouter(
    prefix="/ws",
    tags=['Web']
)

@router.websocket("/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    await manager.connect(websocket,room_id)

    try:
        while True:
            data=await websocket.receive_text()
            
            await manager.broadcast(data,room_id)
    except WebSocketDisconnect:
        await manager.disconnect(websocket,room_id)


    