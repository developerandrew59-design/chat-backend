

import pytest
from schemas import TokenReturn
from jose import jwt
from config import settings

def test_root(client):
    response=client.get("/")
    assert response.json().get('message') == 'it works better!!!'
    assert response.status_code==200

def test_create_user(client):
    response=client.post("/users",json={"email":"docker@gmail.com",
                                        "password":"mail"})
    assert response.status_code==201

def test_login_user(client,test_user):
    response=client.post("/login",data={"username":test_user['email'],
                                        "password":test_user['password']}) 
    login_response=TokenReturn(**response.json())
    payload=jwt.decode(login_response.acess_token,settings.secret_key,algorithms=[settings.algorithm])
    id=payload.get("user_id")

    assert id==test_user['id']
    assert response.status_code==201
    assert login_response.token_type=="bearer"

@pytest.mark.parametrize("email,password,status_code",
                         [('wrong@gmail.com','hello',403),
                         ('hello@gmail.com','wrongpassword',403),
                         ('wrong@gmail.com',"wrong",403),
                         (None,'wrongpassword',422),
                         ('wrong',None,422)]) 
def test_failed_login(client,email,password,status_code):
    response=client.post("/login",data={"username":email,"password":password})

    assert response.status_code==status_code
