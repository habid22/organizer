"""
API routes for file management and organization.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app.services.simple_organizer import SimpleOrganizerService

router = APIRouter()

class OrganizeRequest(BaseModel):
    dry_run: bool = True

@router.get("/")
async def get_files(
    category: Optional[str] = None,
    limit: int = 100
):
    """Get list of files with optional filtering"""
    organizer = SimpleOrganizerService()
    files = organizer.scan_files()
    
    # Filter by category if specified
    if category:
        files = [f for f in files if f["category"].lower() == category.lower()]
    
    # Limit results
    files = files[:limit]
    
    return {
        "files": files,
        "total": len(files),
        "limit": limit
    }

@router.post("/scan")
async def scan_files():
    """Scan downloads folder for files"""
    organizer = SimpleOrganizerService()
    files = organizer.scan_files()
    
    return {
        "message": "Scan completed",
        "files_found": len(files),
        "files": files
    }

@router.post("/organize")
async def organize_files(request: OrganizeRequest):
    """Organize files into categories"""
    organizer = SimpleOrganizerService()
    organized_count, errors, results = organizer.organize_files(dry_run=request.dry_run)
    
    return {
        "message": "Organization completed" if not request.dry_run else "Dry run completed",
        "organized_count": organized_count,
        "errors": errors,
        "results": results,
        "dry_run": request.dry_run
    }

@router.get("/stats")
async def get_stats():
    """Get organization statistics"""
    organizer = SimpleOrganizerService()
    stats = organizer.get_stats()
    
    return stats
