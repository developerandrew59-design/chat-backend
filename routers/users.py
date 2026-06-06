from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from utils import hash
import Oauth2
import logging

logger=logging.getLogger(__name__)

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/",response_model=schemas.UserReturn,status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate,db:Session=Depends(get_db)):
    hashed_password=hash(user.password)
    user.password=hashed_password
    user_dict=models.User(**user.model_dump())
    db.add(user_dict)
    db.commit()
    db.refresh(user_dict)

    logger.info(f"new user created {user_dict.email}")

    return user_dict

@router.get("/",response_model=list[schemas.UserReturn])
def get_all_users(db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    users=db.query(models.User).all()

    logger.info(f"all users fetched by user with user_id {current_user.id}")
    return users


@router.get("/{id}",response_model=schemas.UserReturn)
def get_one_user(id:int,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    user=db.query(models.User).filter(models.User.id==id).first()

    if not user:
        logger.warning(f"User id {id} not found, this request is made by user with id {current_user.id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")
    
    logger.info(f"User with id {id} is fetched by user with id {current_user.id} ")
    return user