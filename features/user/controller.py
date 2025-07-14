
from sqlalchemy.orm import Session
from features.user.schema import UserCreate, UserLogin
from features.user.model import User
from core.security import hash_password
from core.database import get_db
from core.response import Response
import bcrypt

def register_user(user: UserCreate, db: Session):
    response = Response()

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        return response.set(status="user already exists", error_code=409, message="User already exists")

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

    return response.set(status="success", error_code=200, message="User registered successfully", data=new_user)


def login(user: UserLogin, db: Session):
    response = Response()
    print("reached before query")
    check_if_user_exist = db.query(User).filter(User.email == user.email).first()
    print("reached after query")
    print(check_if_user_exist.email,check_if_user_exist.password, "user data")
    is_valid = bcrypt.checkpw(user.password.encode('utf-8'), check_if_user_exist.password.encode('utf-8'))
    return response.set(status="success", error_code=200, message="user data", data=is_valid)