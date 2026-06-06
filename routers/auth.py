import schemas
from fastapi import HTTPException,status,APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from Oauth2 import create_acess_token
from sqlalchemy.orm import Session
from database import get_db
import models
import utils
import logging

logger=logging.getLogger(__name__)

router=APIRouter(
    prefix="/login",
    tags=['Authentication']
)

@router.post("/",response_model=schemas.TokenReturn,status_code=status.HTTP_201_CREATED)
def login_route(users_creds:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==users_creds.username).first()
    if not user:
        logger.warning("Someone's trying to login with a email that does not exict in the database")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid creditinals")
        
    if not utils.verify(users_creds.password,user.password):
        logger.warning(f"User {users_creds.username} is trying to login but does not have the right password")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid creditinals")
    
    logger.info(f"user with email {users_creds.username} just created an acess_token")
    token=create_acess_token(data={"user_id":user.id})

    return {"acess_token":token, "token_type": "bearer"}

