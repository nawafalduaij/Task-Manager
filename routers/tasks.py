"""
Task Router - Handles task-related API endpoints
"""
from fastapi import APIRouter, Query, Depends
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.models import TaskCreate
from database import get_db
from models import Task

# Create router for tasks endpoints
router = APIRouter(prefix="/tasks", tags=["tasks"])


# GET /tasks/ - Get all tasks with optional filtering
@router.get("/")
async def get_tasks(
    status: Annotated[Optional[str], Query(description="Filter by status")] = None,
    priority: Annotated[Optional[str], Query(description="Filter by priority")] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all tasks, optionally filtered by status or priority"""
    query = select(Task)
    
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    tasks_list = [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "priority": t.priority,
            "status": t.status,
            "assigned_to": t.assigned_to
        }
        for t in tasks
    ]
    
    return {"tasks": tasks_list, "count": len(tasks_list)}


# POST /tasks/ - Create a new task
@router.post("/")
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    """Create a new task"""
    # Create new task in database
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        assigned_to=None  # Will be linked by user ID later
    )
    
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    
    task_dict = {
        "id": db_task.id,
        "title": db_task.title,
        "description": db_task.description,
        "priority": db_task.priority,
        "status": db_task.status,
        "assigned_to": db_task.assigned_to
    }
    
    return {"message": "Task created successfully", "task": task_dict}
