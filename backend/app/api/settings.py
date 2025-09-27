"""
API routes for application settings and configuration.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.models.organization_rule import OrganizationRule
from app.core.config import settings

router = APIRouter()

class OrganizationRuleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    file_pattern: str
    file_extension: Optional[str] = None
    file_size_min: Optional[int] = None
    file_size_max: Optional[int] = None
    content_keywords: Optional[str] = None
    target_category: str
    target_folder: str
    rename_pattern: Optional[str] = None
    priority: int = 0

class OrganizationRuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    file_pattern: Optional[str] = None
    file_extension: Optional[str] = None
    file_size_min: Optional[int] = None
    file_size_max: Optional[int] = None
    content_keywords: Optional[str] = None
    target_category: Optional[str] = None
    target_folder: Optional[str] = None
    rename_pattern: Optional[str] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None

@router.get("/")
async def get_settings():
    """Get current application settings"""
    return {
        "downloads_path": settings.downloads_path,
        "supported_extensions": settings.supported_extensions,
        "default_categories": settings.default_categories,
        "cleanup_temp_files_days": settings.cleanup_temp_files_days,
        "cleanup_old_files_days": settings.cleanup_old_files_days,
        "max_file_size_mb": settings.max_file_size_mb
    }

@router.get("/rules")
async def get_organization_rules(
    active_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get organization rules"""
    query = db.query(OrganizationRule)
    
    if active_only:
        query = query.filter(OrganizationRule.is_active == True)
    
    rules = query.order_by(OrganizationRule.priority.desc()).all()
    
    return {"rules": rules}

@router.post("/rules")
async def create_organization_rule(
    rule_data: OrganizationRuleCreate,
    db: Session = Depends(get_db)
):
    """Create a new organization rule"""
    rule = OrganizationRule(**rule_data.dict())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    
    return {"message": "Rule created successfully", "rule": rule}

@router.put("/rules/{rule_id}")
async def update_organization_rule(
    rule_id: int,
    rule_data: OrganizationRuleUpdate,
    db: Session = Depends(get_db)
):
    """Update an organization rule"""
    rule = db.query(OrganizationRule).filter(OrganizationRule.id == rule_id).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    # Update only provided fields
    update_data = rule_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rule, field, value)
    
    db.commit()
    db.refresh(rule)
    
    return {"message": "Rule updated successfully", "rule": rule}

@router.delete("/rules/{rule_id}")
async def delete_organization_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """Delete an organization rule"""
    rule = db.query(OrganizationRule).filter(OrganizationRule.id == rule_id).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    db.delete(rule)
    db.commit()
    
    return {"message": "Rule deleted successfully"}

@router.post("/rules/{rule_id}/toggle")
async def toggle_organization_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """Toggle organization rule active status"""
    rule = db.query(OrganizationRule).filter(OrganizationRule.id == rule_id).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    rule.is_active = not rule.is_active
    db.commit()
    
    return {
        "message": f"Rule {'activated' if rule.is_active else 'deactivated'}",
        "is_active": rule.is_active
    }

@router.get("/categories")
async def get_categories():
    """Get available file categories"""
    return {
        "categories": list(settings.default_categories.keys()),
        "category_extensions": settings.default_categories
    }

@router.post("/test-rule")
async def test_organization_rule(
    rule_data: OrganizationRuleCreate,
    test_files: List[str]
):
    """Test an organization rule against sample files"""
    # This would implement rule testing logic
    # For now, return a simple response
    return {
        "message": "Rule testing not implemented yet",
        "test_files": test_files,
        "rule": rule_data
    }
