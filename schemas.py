from pydantic import BaseModel,EmailStr,ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserReturn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    id:int
    created_at: datetime


class RoomCreate(BaseModel):
    name: str

class RoomOut(RoomCreate):
    id:int
    created_at: datetime

class TokenReturn(BaseModel):
    acess_token: str
    token_type: str    

class TokenData(BaseModel):
    id: int | None = None


class MessageCreate(BaseModel):
    message: str
    room_id: int

class MessageOut(MessageCreate):
    id: int
    account_id: int
    created_at: datetime
        
