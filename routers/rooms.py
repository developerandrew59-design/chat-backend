from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import Oauth2

router=APIRouter(
    prefix="/rooms",
    tags=['Rooms']
)

@router.post("/",response_model=schemas.RoomOut,status_code=status.HTTP_201_CREATED)
def create_room(room: schemas.RoomCreate,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    room_dict=models.Room(**room.model_dump())
    db.add(room_dict)
    db.commit()
    db.refresh(room_dict)

    return room_dict

@router.get("/",response_model=list[schemas.RoomOut])
def get_all_rooms(db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    rooms=db.query(models.Room).all()
    return rooms

@router.get("/{id}",response_model=schemas.RoomOut)
def get_one_room(id:int,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    room=db.query(models.Room).filter(models.Room.id==id).first()
    
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"room with id {id} not found")
    
    return room