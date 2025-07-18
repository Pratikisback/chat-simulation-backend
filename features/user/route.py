from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from core.database import get_db
from features.user import controller, schema
from features.user.model import User
from dependencies.auth import get_current_user
from fastapi import HTTPException
from core.response import Response



router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register_user(user_data: schema.UserCreate, db: Session = Depends(get_db)):
    return controller.register_user(user_data, db)


@router.post("/login")
def login_user(user_data: schema.UserLogin, db: Session = Depends(get_db)):
    return controller.login(user_data, db)  


@router.get("/get-all-users")
async def get_all_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return controller.get_all_users(db)

@router.post("/create-refresh-token")
async def create_refresh_token(request: Request, db: Session = Depends(get_db)):
    response = Response()
    body = await request.json()
    token = body.get("refresh_token")
    
    if not token:
        return response.set(status="Missing refresh token",error_code=400, message="Missing refresh token", data=None)

    return controller.create_refresh_token(token, db)