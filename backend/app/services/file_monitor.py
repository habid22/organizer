"""
File monitoring service for watching the downloads folder.
"""

import os
import asyncio
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import List, Callable

from app.core.config import settings
from app.services.file_organizer import FileOrganizerService

class DownloadsHandler(FileSystemEventHandler):
    """Handler for file system events in the downloads folder"""
    
    def __init__(self, organizer: FileOrganizerService, callback: Callable = None):
        self.organizer = organizer
        self.callback = callback
        self.supported_extensions = settings.supported_extensions
    
    def on_created(self, event):
        """Handle file creation events"""
        if not event.is_directory:
            file_path = event.src_path
            if self._should_organize(file_path):
                # Process file asynchronously
                asyncio.create_task(self._process_file(file_path))
    
    def _should_organize(self, file_path: str) -> bool:
        """Check if file should be organized"""
        file_ext = Path(file_path).suffix.lower()
        return file_ext in self.supported_extensions
    
    async def _process_file(self, file_path: str):
        """Process a new file"""
        try:
            # Wait a moment for file to be fully written
            await asyncio.sleep(1)
            
            # Check if file still exists and is accessible
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                # Organize the file
                result = self.organizer.organize_file(file_path)
                
                # Call callback if provided
                if self.callback:
                    await self.callback(result)
                    
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

class FileMonitorService:
    """Service for monitoring the downloads folder"""
    
    def __init__(self):
        self.organizer = FileOrganizerService()
        self.observer = None
        self.is_monitoring = False
    
    async def start_monitoring(self):
        """Start monitoring the downloads folder"""
        if self.is_monitoring:
            return
        
        downloads_path = settings.downloads_path
        
        # Create downloads folder if it doesn't exist
        os.makedirs(downloads_path, exist_ok=True)
        
        # Set up file system observer
        self.observer = Observer()
        handler = DownloadsHandler(
            self.organizer, 
            callback=self._on_file_organized
        )
        
        self.observer.schedule(
            handler, 
            downloads_path, 
            recursive=settings.watch_recursive
        )
        
        # Start monitoring
        self.observer.start()
        self.is_monitoring = True
        
        print(f"Started monitoring downloads folder: {downloads_path}")
    
    async def stop_monitoring(self):
        """Stop monitoring the downloads folder"""
        if self.observer and self.is_monitoring:
            self.observer.stop()
            self.observer.join()
            self.is_monitoring = False
            print("Stopped monitoring downloads folder")
    
    async def _on_file_organized(self, result: dict):
        """Callback when a file is organized"""
        if result["success"]:
            print(f"Organized: {result['original_path']} -> {result['new_path']}")
        else:
            print(f"Failed to organize: {result['original_path']} - {result['error']}")
    
    def scan_existing_files(self) -> List[dict]:
        """Scan existing files in downloads folder"""
        downloads_path = settings.downloads_path
        results = []
        
        if not os.path.exists(downloads_path):
            return results
        
        for root, dirs, files in os.walk(downloads_path):
            for file in files:
                file_path = os.path.join(root, file)
                if self._should_organize(file_path):
                    # Just scan and add to database, don't organize yet
                    result = self._scan_file(file_path)
                    results.append(result)
        
        return results
    
    def _scan_file(self, file_path: str) -> dict:
        """Scan a file and add to database without organizing"""
        try:
            import os
            from datetime import datetime
            from pathlib import Path
            
            # Get file info
            stat = os.stat(file_path)
            file_size = stat.st_size
            created_time = datetime.fromtimestamp(stat.st_ctime)
            
            # Determine category
            file_ext = Path(file_path).suffix.lower()
            category = None
            for cat, extensions in settings.default_categories.items():
                if file_ext in extensions:
                    category = cat
                    break
            
            # Add to database
            from app.core.database import SessionLocal
            from app.models.file import File
            
            db = SessionLocal()
            try:
                # Check if file already exists
                existing_file = db.query(File).filter(File.original_path == file_path).first()
                if existing_file:
                    return {"success": True, "message": "File already in database", "file_path": file_path}
                
                # Create new file record
                file_record = File(
                    original_name=os.path.basename(file_path),
                    original_path=file_path,
                    file_size=file_size,
                    file_type=file_ext,
                    category=category,
                    created_at=created_time,
                    is_organized=False
                )
                db.add(file_record)
                db.commit()
                
                return {
                    "success": True,
                    "file_path": file_path,
                    "category": category,
                    "message": "File added to database"
                }
            finally:
                db.close()
                
        except Exception as e:
            print(f"Error scanning file {file_path}: {e}")
            return {
                "success": False,
                "file_path": file_path,
                "error": str(e)
            }
    
    def _should_organize(self, file_path: str) -> bool:
        """Check if file should be organized"""
        file_ext = Path(file_path).suffix.lower()
        return file_ext in settings.supported_extensions
