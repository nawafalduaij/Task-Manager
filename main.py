"""
Main FastAPI Application
"""
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

from routers import users, tasks
from database import create_tables

# Import models so Base.metadata knows about tables before create_tables() runs
import models  # noqa: F401

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FRONTEND_DIR = Path(__file__).parent / "frontend"


# Lifespan handler - creates tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables (don't crash app if DB not ready)
    try:
        await create_tables()
        logger.info("Database tables created or already exist.")
    except Exception as e:
        logger.warning("Could not create tables (is DATABASE_URL set?): %s", e)
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

# Serve frontend static files at /app
if FRONTEND_DIR.exists():
    app.mount("/app", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Task API"}


# Redirect /frontend to the app UI
@app.get("/frontend")
async def frontend_redirect():
    return RedirectResponse(url="/app/")


# Health check endpoint for Railway
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
