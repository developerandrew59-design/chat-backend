import pytest
from schemas import MessageOut
from jose import jwt
from config import settings

def test_create_message(authorized_client)