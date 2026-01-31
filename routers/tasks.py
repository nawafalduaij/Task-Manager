"""
Task Router - Handles task-related API endpoints
"""
from fastapi import APIRouter, Query
from typing import Annotated, List, Optional
from schemas.models import TaskCreate

# Create router for tasks endpoints
router = APIRouter(prefix="/tasks", tags=["tasks"])

# In-memory storage
tasks_db: List[dict] = []
task_id_counter = 1

# GET /tasks/ - Get all tasks with optional filtering
@router.get("/")
async def get_tasks(
    status: Annotated[Optional[str], Query(description="Filter by status")] = None,
    priority: Annotated[Optional[str], Query(description="Filter by priority")] = None
):
    """Get all tasks, optionally filtered by status or priority"""
    filtered_tasks = tasks_db
    
    if status:
        filtered_tasks = [t for t in filtered_tasks if t.get("status") == status]
    if priority:
        filtered_tasks = [t for t in filtered_tasks if t.get("priority") == priority]
    
    return {"tasks": filtered_tasks, "count": len(filtered_tasks)}

# POST /tasks/ - Create a new task
@router.post("/")
async def create_task(task: TaskCreate):
    """Create a new task"""
    global task_id_counter
    
    # Convert Pydantic model to dictionary
    task_dict = {
        "id": task_id_counter,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "status": task.status,
        "assigned_to": task.assigned_to
    }
    tasks_db.append(task_dict)
    task_id_counter += 1
    return {"message": "Task created successfully", "task": task_dict}
