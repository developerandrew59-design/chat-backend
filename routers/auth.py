import schemas
from fastapi import HTTPException,status,APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from Oauth2 import create_acess_token
from sqlalchemy.orm import Session
from database import get_db
import models
import utils

router=APIRouter(
    prefix="/login",
    tags=['Authentication']
)

@router.post("/",response_model=schemas.TokenReturn,status_code=status.HTTP_201_CREATED)
def login_route(users_creds:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==users_creds.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid creditinals")
    if not utils.verify(users_creds.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid creditinals")
    token=create_acess_token(data={"user_id":user.id})

    return {"acess_token":token, "token_type": "bearer"}

