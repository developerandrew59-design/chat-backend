from email import message
from database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, null, text


class Message(Base):
    __tablename__='messages'
    id=Column(Integer,primary_key=True,nullable=False)
    message=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    room_id=Column(Integer,ForeignKey("rooms.id",ondelete='CASCADE'),nullable=False)
    account_id=Column(Integer,ForeignKey("accounts.id",ondelete='CASCADE'),nullable=False)

class User(Base):
    __tablename__="accounts"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Room(Base):
    __tablename__='rooms'
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))




        