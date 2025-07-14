from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from features.user import controller, schema


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register_user(user_data: schema.UserCreate, db: Session = Depends(get_db)):
    return controller.register_user(user_data, db)


@router.post("/login")
def login_user(user_data: schema.UserLogin, db: Session = Depends(get_db)):
    return controller.login(user_data, db)  