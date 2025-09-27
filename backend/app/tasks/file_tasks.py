"""
Background tasks for file processing.
"""

from celery import current_task
from app.core.celery import celery_app
from app.services.file_organizer import FileOrganizerService
from app.models.file import File
from app.core.database import SessionLocal
import os

@celery_app.task(bind=True)
def organize_file_task(self, file_path: str):
    """
    Background task to organize a single file.
    
    Args:
        file_path: Path to the file to organize
        
    Returns:
        Dict with organization results
    """
    try:
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Organizing file", "file_path": file_path}
        )
        
        # Organize the file
        organizer = FileOrganizerService()
        result = organizer.organize_file(file_path)
        
        # Save to database if successful
        if result["success"]:
            db = SessionLocal()
            try:
                file_record = File(
                    original_name=os.path.basename(file_path),
                    new_name=result.get("new_name"),
                    original_path=file_path,
                    new_path=result.get("new_path"),
                    file_size=result["file_info"]["size"],
                    file_type=result["file_info"]["extension"],
                    category=result.get("category"),
                    mime_type=result["file_info"]["mime_type"],
                    is_organized=True,
                    checksum=result["file_info"]["checksum"]
                )
                db.add(file_record)
                db.commit()
            finally:
                db.close()
        
        return {
            "status": "completed",
            "result": result
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }

@celery_app.task(bind=True)
def scan_downloads_folder_task(self):
    """
    Background task to scan the entire downloads folder.
    
    Returns:
        Dict with scan results
    """
    try:
        from app.services.file_monitor import FileMonitorService
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Scanning downloads folder"}
        )
        
        # Scan the folder
        monitor = FileMonitorService()
        results = monitor.scan_existing_files()
        
        # Count results
        successful = sum(1 for r in results if r["success"])
        failed = len(results) - successful
        
        return {
            "status": "completed",
            "total_files": len(results),
            "successful": successful,
            "failed": failed,
            "results": results
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }

@celery_app.task(bind=True)
def cleanup_old_files_task(self, days_old: int = 30):
    """
    Background task to cleanup old files.
    
    Args:
        days_old: Files older than this many days will be cleaned up
        
    Returns:
        Dict with cleanup results
    """
    try:
        from datetime import datetime, timedelta
        from app.core.config import settings
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": f"Cleaning up files older than {days_old} days"}
        )
        
        downloads_path = settings.downloads_path
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        cleaned_files = []
        
        # Walk through downloads folder
        for root, dirs, files in os.walk(downloads_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Check file modification time
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_time < cutoff_date:
                        # Delete the file
                        os.remove(file_path)
                        cleaned_files.append(file_path)
                except (OSError, IOError):
                    continue
        
        return {
            "status": "completed",
            "cleaned_files": len(cleaned_files),
            "files": cleaned_files
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }
