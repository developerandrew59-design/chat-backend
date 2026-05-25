from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings
import pytest
from database import get_db,Base

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
        
            



                                  
