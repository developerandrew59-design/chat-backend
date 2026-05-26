from email import message_from_string

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings
import pytest
from main import app
from database import get_db,Base
from Oauth2 import create_acess_token
from models import Room,Message

SQLALCHEMY_DATABASE_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine=create_engine(SQLALCHEMY_DATABASE_URL)

Testingsessionclient=sessionmaker(autoflush=False,autocommit=False,bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=Testingsessionclient()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        yield session
    app.dependency_overrides[get_db]=override_get_db 
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data={"email":"hello@gmail.com",
               "password":"hello"}
    response=client.post("/users",json=user_data)
    new_user=response.json()

    new_user['password']=user_data['password']
    assert response.status_code==201

    return new_user

@pytest.fixture
def test_token(test_user):
    return create_acess_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client,test_token):
    client.headers={
        **client.headers,
        "Authorization": f"Bearer {test_token}"
    }

    return client


@pytest.fixture
def test_room(test_user,session):

    rooms_data = [
    {"name": "Room1"},
    {"name": "Room2"},
    {"name": "Room3"}
]
    
    def test_convert_data_models(room):
        return Room(**room)
    
    room_map=map(test_convert_data_models,rooms_data)
    rooms=list(room_map)

    session.add_all(rooms)

    session.commit()

    rooms=session.query(Room).all()

    return rooms

@pytest.fixture
def test_message(test_user,test_room,session):

    message_data = [
    {"message": "i like this group","room_id":test_room[0].id,"account_id": test_user['id']},
    {"message": "i hate this group","room_id":test_room[1].id,"account_id": test_user['id']},
    {"message": "i feel ambivalent about this group","room_id":test_room[0].id,"account_id": test_user['id']}]


    def test_convert_data_models(message):
        return Message(**message)
    
    message_map=map(test_convert_data_models,message_data)
    messages=list(message_map)

    session.add_all(messages)

    session.commit()

    messages=session.query(Message).all()

    return messages




                    
                    
    






        
            



                                  
