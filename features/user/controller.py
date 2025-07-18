
from sqlalchemy.orm import Session
from features.user.schema import UserCreate, UserLogin
from features.user.model import User
from core.security import hash_password, create_access_token
from core.database import get_db
from core.response import Response
import bcrypt
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import HTTPException
from core.security import decode_token
from jose import jwt, JWTError, ExpiredSignatureError
load_dotenv()


def register_user(user: UserCreate, db: Session):
    response = Response()

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        return response.set(status="user already exists", status_code=409, message="User already exists")

    new_user = User(
        email=user.email,
        name=user.name,
        password=hash_password(user.password),
        role=user.role,
        # assigned_manager=user.assigned_manager,
        # assigned_shift_type=user.assigned_shift_type,
        on_break=user.on_break,
        on_shift=user.on_shift,
        is_deleted=user.is_deleted
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return response.set(status="success", status_code=200, message="User registered successfully", data=new_user)


def login(user: UserLogin, db: Session):
    response = Response()
    user_details = db.query(User).filter(User.email == user.email).first()
    if not user_details:
        return response.set(status="user not found", status_code=404, message="User not found")
    is_valid = bcrypt.checkpw(user.password.encode('utf-8'), user_details.password.encode('utf-8'))
  
    if not is_valid:
        return response.set(status="credentials mismatch", status_code=404, message="password is incorrect")

    access_token = create_access_token(data={"email": user.email, "role": user_details.role}, expires_delta=timedelta(minutes=15))
    refresh_token = create_access_token(data={"email": user.email, "role": user_details.role}, expires_delta=timedelta(days=30)) 

    response_data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "email": user.email
            }
    
    print(response_data)
    return response.set(status="success", status_code=201, message="user logged in", data=response_data)



def create_refresh_token(token: str, db:Session):
    try: 
        response = Response()
        payload = decode_token(token)
        if isinstance(payload, dict) and "error" in payload:
            if payload["error"] == "signature_expired":
                return response.set(status="token expired", status_code=401, message="Token has expired", data=None)
            elif payload["error"] == "invalid_token":
                return response.set(status="invalid token", status_code=401, message="Token is invalid", data=None)
        data = {
           
            "refresh_token": create_access_token(data={"email": payload["email"], "role": payload["role"]}, expires_delta=timedelta(minutes=15))
        } 
        return response.set(status="success", status_code=200, message="refresh token created", data=data)
    except ExpiredSignatureError:
        return response.set(status=200, status_code=200, message="Token has expired", data=None)
    except JWTError:
        return response.set(status="invalid token", status_code=401, message="Token is invalid", data=None) 




def get_all_users(db: Session):
    response = Response()
    users = db.query(User).all()
    return response.set(status="success", status_code=200, message="user data", data=users)