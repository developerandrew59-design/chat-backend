import re
from urllib import response

import pytest
from schemas import MessageOut
from jose import jwt
from config import settings
from tests.conftest import authorized_client


def test_create_message(authorized_client,test_room):
    data={"message":"hey there",
          "room_id":test_room[0].id}
    response=authorized_client.post("/messages",json=data)

    assert response.status_code==201

def test_get_all_messages(authorized_client,test_room):
    response=authorized_client.get(f"/messages?room_id={test_room[0].id}")

    assert response.status_code==200    

def test_get_one_message(authorized_client,test_message):
    response=authorized_client.get(f"/messages/{test_message[0].id}")

    assert response.status_code==200    


def test_get_one_message_non_exitent(authorized_client):
    response=authorized_client.get("/messages/594834")

    assert response.status_code==404

def test_create_message_unauthorized_user(client,test_room):
    data={"message":"hey there",
          "room_id":test_room[0].id}
    response=client.post("/messages",json=data)

    assert response.status_code==401 

def test_get_all_messages_unauthorized_user(client,test_room):
    response=client.get(f"/messages?{test_room[0].id}")  

    assert response.status_code==401     
