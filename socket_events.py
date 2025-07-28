from state import connected_users
from dotenv import load_dotenv
from jose import jwt, JWTError
import os
from features.messages.model import ChatMessage
from core.database import SessionLocal
load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")

def register_socket_events(sio):
    @sio.event
    async def connect(sid, environ):
        print(f"[SOCKET] New connection: {sid}")
        headers = environ.get("asgi.scope", {}).get("headers", [])
        cookie_header = next((val for key, val in headers if key == b"cookie"), b"").decode()
        
        cookies = dict(cookie.split("=") for cookie in cookie_header.split("; ") if "=" in cookie)
        token = cookies.get("access_token")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) 
            print(payload.get("email"),  "payload")
            
            if not payload:
                print("[SOCKET] No email found in token")
                return False
            
            
            connected_users[payload.get("email")] = sid
            print(f"[SOCKET] User {payload} connected with sid {sid}")
        except JWTError:
            print("[SOCKET] Invalid or missing token")
            return False  # Reject socket connection

    
    @sio.event
    async def disconnect(sid):
        for user, user_id in list(connected_users.items()):
            if user_id == sid:
                del connected_users[user]
                break
        
    
    @sio.event
    async def login(sid, environ):
        headers = environ.get("asgi.scope", {}).get("headers", [])
        cookie_header = next((val for key, val in headers if key == b"cookie"), b"").decode()
        cookies = dict(cookie.split("=") for cookie in cookie_header.split("; ") if "=" in cookie)

        token = cookies.get("access_token")

        try:
            email = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            
            if email:
                connected_users[email] = sid
                print(f"{email} logged in via socket")
        except JWTError:
            print("Invalid or missing token")

    @sio.event
    async def private_message(sid, data):
        sender = data.get("sender")
        recipient = data.get("recipient")
        message = data.get("message")

        recipient_id = connected_users.get(recipient)

        db = SessionLocal()

        try:
            new_msg = ChatMessage(sender=sender, recipient=recipient, message=message)
            db.add(new_msg)
            db.commit()
        finally:
            db.close()

        recipient_id = connected_users.get(recipient)
        print("Connected Users:", connected_users)

        if recipient_id:
            await sio.emit("private_message", data, to=recipient_id)
        await sio.emit("private_message", data, to=sid)