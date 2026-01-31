"""
Data Models (Schemas) for the Task Management System
These define what data looks like and validate it
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Annotated

# Profile model - stores user contact information
class Profile(BaseModel):
    email: str = Field(..., description="User email address")
    phone: str = Field(..., description="User phone number")
    address: str = Field(default="", description="User address (optional)")

# User model - stores user information with nested Profile
class UserCreate(BaseModel):
    username: str = Field(..., description="Unique username")
    # Literal means only these 3 values are allowed
    role: Literal["admin", "manager", "team member"] = Field(..., description="User role")
    # Nested model - Profile is inside UserCreate
    profile: Profile = Field(..., description="User profile information")

# Task model - stores task information
class TaskCreate(BaseModel):
    # Annotated adds extra information about the field
    title: Annotated[str, Field(..., description="Task title (must be capitalized)")]
    description: str = Field(default="", description="Task description (optional)")
    # Priority must be one of these 3 values
    priority: Annotated[Literal["low", "medium", "high"], Field(..., description="Task priority level")]
    # Status must be one of these 3 values
    status: Literal["pending", "in_progress", "completed"] = Field(default="pending", description="Task status")
    assigned_to: str = Field(default="", description="Username of assigned user (optional)")

    # Custom validator - checks if title starts with capital letter
    @field_validator('title')
    @classmethod
    def title_must_be_capitalized(cls, v: str) -> str:
        if not v[0].isupper():
            raise ValueError('Title must start with a capital letter')
        return v
