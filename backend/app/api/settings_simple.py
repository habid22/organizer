"""
Simplified API routes for application settings - no database required.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter()

class OrganizationRuleCreate(BaseModel):
    name: str
    pattern: str
    category: str
    rename_pattern: Optional[str] = None

class OrganizationRuleUpdate(BaseModel):
    name: Optional[str] = None
    pattern: Optional[str] = None
    category: Optional[str] = None
    rename_pattern: Optional[str] = None

@router.get("/")
async def get_settings():
    """Get application settings"""
    return {
        "downloads_path": settings.downloads_path,
        "watch_recursive": settings.watch_recursive,
        "max_file_size_mb": settings.max_file_size_mb,
        "supported_extensions": settings.supported_extensions,
        "default_categories": settings.default_categories,
        "cleanup_temp_files_days": settings.cleanup_temp_files_days,
        "cleanup_old_files_days": settings.cleanup_old_files_days
    }

@router.get("/rules")
async def get_organization_rules():
    """Get all organization rules (simplified - no database)"""
    # Return default categories for simple organizer
    return {
        "categories": {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".avif"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
            "Spreadsheets": [".xlsx", ".xls", ".csv"],
            "Presentations": [".ppt", ".pptx"],
            "Videos": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".m4a"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Software": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
            "Other": []
        }
    }

@router.post("/rules")
async def create_organization_rule(rule: OrganizationRuleCreate):
    """Create a new organization rule (simplified - no database)"""
    return {"message": "Rules are managed by the simple organizer", "rule": rule.dict()}

@router.put("/rules/{rule_id}")
async def update_organization_rule(rule_id: int, rule: OrganizationRuleUpdate):
    """Update an organization rule (simplified - no database)"""
    return {"message": "Rules are managed by the simple organizer", "rule": rule.dict()}

@router.delete("/rules/{rule_id}")
async def delete_organization_rule(rule_id: int):
    """Delete an organization rule (simplified - no database)"""
    return {"message": "Rules are managed by the simple organizer"}
