class ConnectionManager():
    def __init__(self):
        self.active_connection={}
    async def connect(self,websocket,room_id):
        await websocket.accept()

        if room_id not in self.active_connection:
            self.active_connection[room_id]=[]

        self.active_connection[room_id].append(websocket)  

    async def disconnect(self,websocket,room_id):
        self.active_connection[room_id].remove(websocket)

        if len(self.active_connection[room_id])==0:
            del self.active_connection[room_id]   

    async def broadcast(self,message,room_id):
        for connection in self.active_connection[room_id]:
            await connection.send_text(message)    

manager = ConnectionManager()                    
    

         
       

