#!/usr/bin/env python3
"""
Ultra-simple FastAPI backend for testing
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import os

app = FastAPI(
    title="Downloads Organizer API",
    description="Simple file organizer",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OrganizeRequest(BaseModel):
    dry_run: bool = True

# Health check
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Downloads Organizer API is running"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Downloads Organizer API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

# Mock files endpoint - returns fake data instantly
@app.get("/api/files")
async def get_files():
    """Get list of files - MOCK DATA"""
    mock_files = [
        {
            "name": "document.pdf",
            "path": "C:\\Users\\hassa\\Downloads\\document.pdf",
            "category": "Documents",
            "size": 1024000,
            "size_mb": 1.0,
            "created": "2025-09-27T10:00:00",
            "extension": ".pdf"
        },
        {
            "name": "image.jpg",
            "path": "C:\\Users\\hassa\\Downloads\\image.jpg",
            "category": "Images",
            "size": 2048000,
            "size_mb": 2.0,
            "created": "2025-09-27T11:00:00",
            "extension": ".jpg"
        },
        {
            "name": "video.mp4",
            "path": "C:\\Users\\hassa\\Downloads\\video.mp4",
            "category": "Videos",
            "size": 10485760,
            "size_mb": 10.0,
            "created": "2025-09-27T12:00:00",
            "extension": ".mp4"
        }
    ]
    
    return {
        "files": mock_files,
        "total": len(mock_files),
        "limit": 100
    }

# Mock scan endpoint
@app.post("/api/files/scan")
async def scan_files():
    """Scan files - MOCK RESPONSE"""
    return {
        "message": "Scan completed",
        "files_found": 3,
        "files": [
            {
                "name": "document.pdf",
                "path": "C:\\Users\\hassa\\Downloads\\document.pdf",
                "category": "Documents"
            }
        ]
    }

# Mock organize endpoint
@app.post("/api/files/organize")
async def organize_files(request: OrganizeRequest):
    """Organize files - MOCK RESPONSE"""
    return {
        "message": "Organization completed" if not request.dry_run else "Dry run completed",
        "organized_count": 3,
        "errors": [],
        "results": [
            {
                "original_path": "C:\\Users\\hassa\\Downloads\\document.pdf",
                "new_path": "C:\\Users\\hassa\\Downloads\\Organized\\Documents\\document_2025-09-27_10-00.pdf",
                "action": "Would move" if request.dry_run else "Moved"
            }
        ],
        "dry_run": request.dry_run
    }

# Mock stats endpoint
@app.get("/api/files/stats")
async def get_stats():
    """Get stats - MOCK RESPONSE"""
    return {
        "total_scanned": 3,
        "total_organized": 0,
        "categories": {
            "Documents": 1,
            "Images": 1,
            "Videos": 1,
            "Software": 0,
            "Archives": 0,
            "Audio": 0,
            "Other": 0
        }
    }

# Mock dashboard endpoints
@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    return {
        "total_files": 3,
        "organized_files": 0,
        "categories": {
            "Documents": 1,
            "Images": 1,
            "Videos": 1
        }
    }

@app.get("/api/dashboard/activity")
async def get_recent_activity():
    return {
        "activities": [
            {
                "id": 1,
                "action": "file_organized",
                "file_name": "document.pdf",
                "timestamp": "2025-09-27T10:00:00"
            }
        ]
    }

@app.get("/api/dashboard/folders")
async def get_folder_structure():
    return {
        "folders": [
            {
                "name": "Documents",
                "path": "C:\\Users\\hassa\\Downloads\\Organized\\Documents",
                "file_count": 0
            }
        ]
    }

@app.get("/api/dashboard/storage")
async def get_storage_info():
    return {
        "total_size": 13824000,
        "organized_size": 0,
        "available_space": 1000000000
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
