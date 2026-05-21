from re import M

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import Oauth2

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

    return message_dict

@router.get("/",response_model=list[schemas.MessageOut])
def get_all_messages(room_id:int,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    messages=db.query(models.Message).filter(models.Message.room_id==room_id).all()

    return messages

@router.get("/{id}",response_model=schemas.MessageOut)
def get_one_message(id:int,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    message=db.query(models.Message).filter(models.Message.id==id).first()

    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message with id {id} not found")
    
    if not message.account_id==current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='not authorized to perform such action')
    
    return message
