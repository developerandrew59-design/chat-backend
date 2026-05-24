from fastapi import APIRouter, Depends, HTTPException,WebSocket,WebSocketDisconnect,status
from websocket_manager import manager
from sqlalchemy.orm import Session
from database import get_db
from Oauth2 import verify_acess_token
import models

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

    try:
        while True:
            data=await websocket.receive_text()
            save_message=models.Message(message=data,room_id=room_id,account_id=token_data.id)
            db.add(save_message)
            db.commit()
                        
            await manager.broadcast(data,room_id)
    except WebSocketDisconnect:
        await manager.disconnect(websocket,room_id)


    