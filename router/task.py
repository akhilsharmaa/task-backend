from datetime import datetime, timedelta, timezone
from typing import Optional, List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from services.database import db_dependency
from models.task import Task  
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from enum import Enum
import json

router = APIRouter(
    prefix="/tasks",
    tags=["Task"],
    responses={404: {"description": "Not found"}},
)

class TaskBase(BaseModel):
    title: str
    description: str 
    is_completed: bool 

@router.post("")
async def create_new_task(task: TaskBase,
                          db: db_dependency):

    db_task = Task(
        title=task.title,
        description=task.description, 
        is_completed=task.is_completed, 
    )

    try:
        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        return JSONResponse(
            status_code=200,
            content={
                "message": "Successfully added the task.",
            }
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A task already exists."
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add new task. Error: {str(e)}"
        )

@router.get("")
async def view_all_tasks(db: db_dependency): 
    try: 
        tasks = []  
        db_tasks = db.query(Task).filter().all() 
                    
        for db_task in db_tasks:
                task_data = {
                    "id": db_task.id,
                    "title": db_task.title,
                    "description": db_task.description, 
                    "is_completed": db_task.is_completed, 
                    "created_at": db_task.created_at.isoformat(),  
                }
                tasks.append(task_data) 

        return JSONResponse(
            status_code=200,
            content=tasks
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch all tasks. Error: {str(e)}"
        )


@router.delete("/{task_id}")
async def edit_task(task_id: str, db: db_dependency):
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()

        if db_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found."
            )

        db.delete(db_task)
        db.commit() 
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Successfully deleted the task."
            }
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task. {str(e)}"
        )

@router.put("/{task_id}")
async def edit_task(task_id: str, task: TaskBase, db: db_dependency):
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()

        if db_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found."
            )

        # Update the task fields
        db_task.title = task.title
        db_task.description = task.description
        db_task.is_completed = task.is_completed 

        db.commit()
        db.refresh(db_task)

        # Prepare response data
        task_data = {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "is_completed": db_task.is_completed
        }

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Successfully edited the task.",
                "task": task_data
            }
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to edit task. {str(e)}"
        )
