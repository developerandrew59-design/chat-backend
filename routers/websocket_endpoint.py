from fastapi import APIRouter, Depends, HTTPException,WebSocket,WebSocketDisconnect,status
from websocket_manager import manager
from sqlalchemy.orm import Session
from database import get_db
from Oauth2 import verify_acess_token
import models
import asyncio
import logging

logger=logging.getLogger(__name__)

router=APIRouter(
    prefix="/ws",
    tags=['Web']
)

@router.websocket("/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int,token: str,db:Session=Depends(get_db)):
   

    credentials_exception=HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                        detail="invalid creditinals",
                                        headers={"WWW-Authenticate":"bearer"})

    token_data = verify_acess_token(token, credentials_exception)

    await manager.connect(websocket,room_id)
    asyncio.create_task(manager.listen(room_id))
    logger.info(f"User with id {token_data.id} is connected to room {room_id}")

    try:
        while True:
            data=await websocket.receive_text()
            save_message=models.Message(message=data,room_id=room_id,account_id=token_data.id)
            db.add(save_message)
            db.commit()
            logger.info(f"User with id {token_data.id} just got his/her message broadcasted")            
            await manager.broadcast(data,room_id)
            
            
    except WebSocketDisconnect:
        await manager.disconnect(websocket,room_id)
        logger.info(f"User with id {token_data.id} just got disconnected from room with id {room_id}")


    