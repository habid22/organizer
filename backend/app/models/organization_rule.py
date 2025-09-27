"""
Organization rule model for custom file organization rules.
"""

from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class OrganizationRule(Base):
    """Organization rule model for custom file organization"""
    
    __tablename__ = "organization_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Rule conditions
    file_pattern = Column(String(200), nullable=False)  # File name pattern
    file_extension = Column(String(20), nullable=True)  # Specific extension
    file_size_min = Column(Integer, nullable=True)  # Minimum size in bytes
    file_size_max = Column(Integer, nullable=True)  # Maximum size in bytes
    content_keywords = Column(Text, nullable=True)  # Keywords in content
    
    # Rule actions
    target_category = Column(String(50), nullable=False)
    target_folder = Column(String(200), nullable=False)
    rename_pattern = Column(String(200), nullable=True)  # New name pattern
    
    # Rule settings
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)  # Higher priority rules run first
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<OrganizationRule(id={self.id}, name='{self.name}', pattern='{self.file_pattern}')>"
