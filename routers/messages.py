from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import Oauth2
import logging

logger=logging.getLogger(__name__
                         )

router=APIRouter(
    prefix="/messages",
    tags=['Messages']
)

@router.post("/",response_model=schemas.MessageOut,status_code=status.HTTP_201_CREATED)
def create_Message(message:schemas.MessageCreate,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    message_dict=models.Message(account_id=current_user.id,**message.model_dump())
    db.add(message_dict)
    db.commit()
    db.refresh(message_dict)

    logger.info(f" User with id {current_user.id} just made a message")

    return message_dict

@router.get("/",response_model=list[schemas.MessageOut])
def get_all_messages(room_id:int,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    messages=db.query(models.Message).filter(models.Message.room_id==room_id).all()

    logger.info(f"User with id {current_user.id} just made a request that the user wants to acess all the messages inside the room")
    return messages

@router.get("/{id}",response_model=schemas.MessageOut)
def get_one_message(id:int,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    message=db.query(models.Message).filter(models.Message.id==id).first()

    if not message:
        logger.warning(f"User with id {current_user.id} just made a request to see a message but that message does not exict")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message with id {id} not found")
    
    if not message.account_id==current_user.id:
        logger.warning(f"Message response made by an unauthorized user was denied ")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='not authorized to perform such action')
    logger.info(f" User with id {current_user.id} just wanted to acess an message with id {id}")
    return message
