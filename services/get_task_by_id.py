from models.task import Task 
from fastapi import APIRouter, Depends, HTTPException, status
from services.database import db_dependency

def get_task_by_id(id:int, db: db_dependency): 
    
    try: 
        # Checking the product exist on not   
        db_task = db.query(Task).filter(Task.id == id).first();  
        
        if db_task is None:  
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {id} not exist, please check the task id."
            )
        
        return db_task
    
    except Exception as e:
        # Catch any other unexpected errors
        db.rollback()  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to find task.  Error: {str(e)}"
        )