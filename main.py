from fastapi import FastAPI
from route.routes import router
import socketio
from core.database import get_db, engine
from features.user.model import Base

from socket_events import register_socket_events
from fastapi.middleware.cors import CORSMiddleware
from features.user.route import router as user_route
from route.routes import router

app = FastAPI()
app.include_router(router)
app.include_router(user_route)

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
socket_app = socketio.ASGIApp(sio, app)
register_socket_events(sio)     


origins = [
    "http://192.168.0.108:3000", "http://192.168.1.29:3000", "*" #Use your frontend's actual IP/port here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Required for CORS, you can set it to ["*"] to allow all origins, but it's better to specify your frontend's URL
    allow_credentials=True,        #Required for cookies, so keep it now, If you don't need cookies, you can set it to False, but I am using it for authentication, so please keep it True
    allow_methods=["*"],        # Required for CORS, you can set it to ["*"] to allow all methods, but it's better to specify the methods you need
    allow_headers=["*"],    # Required for CORS, you can set it to ["*"] to allow all headers, but it's better to specify the headers you need
)

Base.metadata.create_all(bind=engine)