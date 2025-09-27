"""
File model for tracking organized files and their metadata.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
from sqlalchemy.sql import func
from app.core.database import Base

class File(Base):
    """File model for tracking organized files"""
    
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    original_name = Column(String(255), nullable=False)
    new_name = Column(String(255), nullable=True)
    original_path = Column(String(500), nullable=False)
    new_path = Column(String(500), nullable=True)
    file_size = Column(Float, nullable=False)  # Size in bytes
    file_type = Column(String(50), nullable=False)
    category = Column(String(50), nullable=True)
    mime_type = Column(String(100), nullable=True)
    
    # Organization metadata
    is_organized = Column(Boolean, default=False)
    is_duplicate = Column(Boolean, default=False)
    duplicate_of = Column(Integer, nullable=True)  # ID of original file
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    organized_at = Column(DateTime(timezone=True), nullable=True)
    last_accessed = Column(DateTime(timezone=True), nullable=True)
    
    # Additional metadata
    download_url = Column(Text, nullable=True)
    checksum = Column(String(64), nullable=True)  # For duplicate detection
    tags = Column(Text, nullable=True)  # JSON string of tags
    
    def __repr__(self):
        return f"<File(id={self.id}, name='{self.original_name}', category='{self.category}')>"
