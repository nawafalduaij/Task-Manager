"""
User Router - Handles user-related API endpoints
"""
from fastapi import APIRouter, Query, Depends
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.models import UserCreate
from database import get_db
from models import User

# Create router for users endpoints
router = APIRouter(prefix="/users", tags=["users"])


# GET /users/ - Get all users with optional filtering
@router.get("/")
async def get_users(
    role: Annotated[Optional[str], Query(description="Filter by role")] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all users, optionally filtered by role"""
    query = select(User)
    
    if role:
        query = query.where(User.role == role)
    
    result = await db.execute(query)
    users = result.scalars().all()
    
    users_list = [
        {
            "id": u.id,
            "username": u.username,
            "role": u.role,
            "profile": {
                "email": u.email,
                "phone": u.phone,
                "address": u.address
            }
        }
        for u in users
    ]
    
    return {"users": users_list, "count": len(users_list)}


# POST /users/ - Create a new user
@router.post("/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user"""
    # Create new user in database
    db_user = User(
        username=user.username,
        role=user.role,
        email=user.profile.email,
        phone=user.profile.phone,
        address=user.profile.address
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    user_dict = {
        "id": db_user.id,
        "username": db_user.username,
        "role": db_user.role,
        "profile": {
            "email": db_user.email,
            "phone": db_user.phone,
            "address": db_user.address
        }
    }
    
    return {"message": "User created successfully", "user": user_dict}
