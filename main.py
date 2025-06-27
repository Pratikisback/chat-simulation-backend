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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)