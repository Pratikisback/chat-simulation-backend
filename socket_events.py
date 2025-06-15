from state import connected_users

def register_socket_events(sio):
    @sio.event
    async def connect(sid, environ):
        print(f"{sid} is connected")

    
    @sio.event
    async def disconnect(sid):
        for user, user_id in list(connected_users.items()):
            if user_id == sid:
                del connected_users[user]
                break
        
    
    @sio.event
    async def login(sid, username):
        connected_users[username] = sid
        print(f"{username} logged in with {sid} to the server, not connected yet")

    @sio.event
    async def private_message(sid, data):
        sender = data.get("sender")
        recipient = data.get("recipient")
        message = data.get("message")

        recipient_id = connected_users.get(recipient)

        if recipient_id:
            await sio.emit(
                "private_message",
                {"sender": sender, "recipient": recipient, "message": message},
                to=recipient_id
            )
            await sio.emit(
                "private_message",
                {"sender": sender, "recipient": recipient, "message": message},
                to=sid
            )
        else:
            print(f" User '{recipient}' not found in connected_users: {connected_users}")