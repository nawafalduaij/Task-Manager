"""
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, tasks

# Create the FastAPI app
app = FastAPI(title="Task Management System API")

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
