from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db

from models import ChatMessage

router = APIRouter()

@router.get("/chat/history")
def get_chat_history(user1: str, user2: str, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).filter(
        ((ChatMessage.sender == user1) & (ChatMessage.recipient == user2)) |
        ((ChatMessage.sender == user2) & (ChatMessage.recipient == user1))
    ).order_by(ChatMessage.timestamp).all()

    return {"messages": [m.__dict__ for m in messages]}
