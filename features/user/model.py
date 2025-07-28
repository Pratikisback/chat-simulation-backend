from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    role = Column(String, default="user") 
    password = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False) 
    # assigned_manager = Column(Integer, ForeignKey("users.id"), nullable=True)
    # assigned_shift_type = Column(Integer, ForeignKey("shift_types.id"), nullable=True)
    on_break = Column(Boolean, default=False)
    on_shift = Column(Boolean, default=False)

