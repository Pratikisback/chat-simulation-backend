
from sqlalchemy.orm import Session
from features.user.schema import UserCreate
from features.user.model import User
from core.security import hash_password
from core.database import get_db
from core.response import Response

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
