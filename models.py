"""
SQLAlchemy Database Models for PostgreSQL
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)  # admin, manager, team member
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, default="")
    
    # Relationship to tasks
    tasks = relationship("Task", back_populates="assignee")


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    priority = Column(String, nullable=False)  # low, medium, high
    status = Column(String, default="pending")  # pending, in_progress, completed
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationship to user
    assignee = relationship("User", back_populates="tasks")
