from urllib import response

import pytest
from schemas import RoomOut
from jose import jwt
from config import settings


@pytest.mark.parametrize("name",[
    ("Group1"),
    ("Group2")
])
def test_create_room(authorized_client,name):
    response=authorized_client.post("/rooms",json={"name":name})

    res_dict=RoomOut(**response.json())

    assert response.status_code==201
    assert res_dict.name==name

def test_get_all_rooms(authorized_client):
    response=authorized_client.get("/rooms")
    assert response.status_code==200  

def test_get_one_room(authorized_client,test_room):
    response=authorized_client.get(f"/rooms/{test_room[0].id}")
    room_dict=RoomOut(**response.json())

    assert response.status_code==200      

def test_unauthorized_get_all_rooms(client,test_room):
    response=client.get("/rooms")
    assert response.status_code==401    