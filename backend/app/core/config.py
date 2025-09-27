"""
Configuration settings for the Downloads Organizer application.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "sqlite:///./downloads_organizer.db"
    
    # Redis for Celery
    redis_url: str = "redis://localhost:6379/0"
    
    # File monitoring
    downloads_path: str = r"C:\Users\hassa\Downloads"
    watch_recursive: bool = True
    
    # File organization
    max_file_size_mb: int = 100  # Skip files larger than 100MB
    supported_extensions: list = [
        ".pdf", ".doc", ".docx", ".txt", ".rtf",
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg",
        ".mp4", ".avi", ".mov", ".wmv", ".flv",
        ".mp3", ".wav", ".flac", ".aac",
        ".zip", ".rar", ".7z", ".tar", ".gz",
        ".exe", ".msi", ".dmg", ".pkg",
        ".xlsx", ".xls", ".csv", ".ppt", ".pptx"
    ]
    
    # Organization rules
    default_categories: dict = {
        "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
        "documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
        "spreadsheets": [".xlsx", ".xls", ".csv"],
        "presentations": [".ppt", ".pptx"],
        "videos": [".mp4", ".avi", ".mov", ".wmv", ".flv"],
        "audio": [".mp3", ".wav", ".flac", ".aac"],
        "archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "software": [".exe", ".msi", ".dmg", ".pkg"]
    }
    
    # Cleanup rules
    cleanup_temp_files_days: int = 7
    cleanup_old_files_days: int = 30
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Downloads Organizer"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
