"""
User Router - Handles user-related API endpoints
"""
from fastapi import APIRouter, Query
from typing import Annotated, List, Optional
from schemas.models import UserCreate

# Create router for users endpoints
router = APIRouter(prefix="/users", tags=["users"])

# In-memory storage
users_db: List[dict] = []

# GET /users/ - Get all users with optional filtering
@router.get("/")
async def get_users(
    role: Annotated[Optional[str], Query(description="Filter by role")] = None
):
    """Get all users, optionally filtered by role"""
    filtered_users = users_db
    
    if role:
        filtered_users = [u for u in filtered_users if u.get("role") == role]
    
    return {"users": filtered_users, "count": len(filtered_users)}

# POST /users/ - Create a new user
@router.post("/")
async def create_user(user: UserCreate):
    """Create a new user"""
    # Convert Pydantic model to dictionary
    user_dict = {
        "username": user.username,
        "role": user.role,
        "profile": {
            "email": user.profile.email,
            "phone": user.profile.phone,
            "address": user.profile.address
        }
    }
    users_db.append(user_dict)
    return {"message": "User created successfully", "user": user_dict}
