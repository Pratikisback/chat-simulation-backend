from typing import Literal
from pydantic import Field, BaseModel


class User(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    age: int = Field(..., min_length=2, max_length=2)
    email: str = Field(..., regex=r'^\S+@\S+\.\S+$')
    role: Literal["manager", "admin", "employee"]
    password: str