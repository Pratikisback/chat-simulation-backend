from fastapi import FastAPI
from route.route import router
import socketio

from socket_events import register_socket_events
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(router)

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
socket_app = socketio.ASGIApp(sio, app)
register_socket_events(sio)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)