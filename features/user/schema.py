from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)
    role: str = Field(default="user", max_length=20)
    # assigned_manager: Optional[int] = None
    # assigned_shift_type: Optional[int] = None
    on_break: bool = False
    on_shift: bool = False  
    is_deleted: bool = False

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str