from fastapi import FastAPI
import models
from database import engine, Base
from routers import users,rooms,auth,messages,websocket_endpoint

models.Base.metadata.create_all(bind=engine)
app=FastAPI()

app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(auth.router)
app.include_router(messages.router)
app.include_router(websocket_endpoint.router)

@app.get("/")
def get_root():
    return {"message":"it works better!!!"}

