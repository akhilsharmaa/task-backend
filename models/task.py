from services.database import Base 
from services.database import Base 
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Enum, Boolean
from enum import Enum as PyEnum 

class Task(Base):
    __tablename__ = "task"
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    title               = Column(String(100), unique=False, nullable=False)
    description         = Column(String(250), unique=False, nullable=True)  
    is_completed         = Column(Boolean, nullable=False, default=False)  
    created_at          = Column(DateTime, default=func.now(), nullable=False)