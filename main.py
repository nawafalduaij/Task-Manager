"""
Main FastAPI Application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, tasks
from database import create_tables


# Lifespan handler - creates tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    await create_tables()
    yield
    # Shutdown: cleanup if needed


# Create the FastAPI app
app = FastAPI(title="Task Management System API", lifespan=lifespan)

# Add CORS middleware (for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(users.router)
app.include_router(tasks.router)


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Task API"}


# Health check endpoint for Railway
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
