from fastapi import Depends
from config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session 
from typing import Annotated

engine =  create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables(): 
    Base.metadata.create_all(bind=engine)
    
def get_db(): 
    db = SessionLocal()
    
    try: 
        yield db; 
    finally: 
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]