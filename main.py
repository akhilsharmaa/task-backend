import os
from os.path import join, dirname 
from fastapi import Depends, FastAPI
from router import task
from services.database import create_tables
from fastapi.middleware.cors import CORSMiddleware
from utils.logger import logger
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task.router)     

create_tables()

@app.get("/")
async def root():
    logger.info(f"New Request at '/' ")

    return {
                "message": "welcome to server",
            }
    
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)