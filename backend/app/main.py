"""
Downloads Organizer - FastAPI Application
Main application entry point with API routes and middleware.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.api import files, dashboard, settings
from app.core.config import settings as app_settings
# No database needed - using simple file operations

# Initialize FastAPI app
app = FastAPI(
    title="Downloads Organizer API",
    description="Intelligent file organization system for managing downloads",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(files.router, prefix="/api/files", tags=["files"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(settings.router, prefix="/api/settings", tags=["settings"])

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Downloads Organizer API is running"}

# Simple health check for Railway
@app.get("/health")
async def simple_health_check():
    return {"status": "ok"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Downloads Organizer API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

# No file monitoring needed - using simple file operations

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
