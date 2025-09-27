#!/usr/bin/env python3
"""
Working FastAPI backend - Fixed async issues
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
import shutil
from datetime import datetime
from pathlib import Path

app = FastAPI(
    title="Downloads Organizer API",
    description="Working file organizer",
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

# Simple file organizer class (no async issues)
class FileOrganizer:
    def __init__(self):
        self.downloads_path = r"C:\Users\hassa\Downloads"
        self.organized_path = os.path.join(self.downloads_path, "Organized")
        self.categories = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".avif"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
            "Software": [".exe", ".msi", ".dmg", ".app", ".deb", ".rpm"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"],
            "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
            "Other": []
        }
    
    def get_category(self, file_path: str) -> str:
        ext = Path(file_path).suffix.lower()
        for category, extensions in self.categories.items():
            if ext in extensions:
                return category
        return "Other"
    
    def generate_smart_name(self, file_path: str, category: str) -> str:
        path = Path(file_path)
        timestamp = datetime.fromtimestamp(path.stat().st_ctime).strftime("%Y-%m-%d_%H-%M")
        name = path.stem
        ext = path.suffix
        
        if "screenshot" in name.lower():
            return f"screenshot_{timestamp}{ext}"
        elif "img" in name.lower() and len(name) < 10:
            return f"photo_{timestamp}{ext}"
        elif category == "Documents" and any(word in name.lower() for word in ["invoice", "report", "document"]):
            return f"{name}_{timestamp}{ext}"
        else:
            return f"{name}_{timestamp}{ext}"
    
    def scan_files(self, max_files: int = 100) -> List[Dict]:
        files = []
        
        if not os.path.exists(self.downloads_path):
            return files
        
        try:
            for filename in os.listdir(self.downloads_path)[:max_files]:
                file_path = os.path.join(self.downloads_path, filename)
                
                if os.path.isdir(file_path) or "Organized" in file_path:
                    continue
                
                try:
                    category = self.get_category(file_path)
                    file_size = os.path.getsize(file_path)
                    created_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    files.append({
                        "name": filename,
                        "path": file_path,
                        "category": category,
                        "size": file_size,
                        "size_mb": round(file_size / (1024 * 1024), 2),
                        "created": created_time.isoformat(),
                        "extension": Path(file_path).suffix.lower()
                    })
                except (OSError, IOError):
                    continue
        except (OSError, IOError):
            pass
        
        return files
    
    def organize_files(self, dry_run: bool = True) -> tuple:
        files = self.scan_files()
        organized_count = 0
        errors = []
        results = []
        
        if not files:
            return organized_count, errors, results
        
        if not dry_run:
            os.makedirs(self.organized_path, exist_ok=True)
        
        for file_info in files:
            original_path = file_info["path"]
            category = file_info["category"]
            
            target_dir = os.path.join(self.organized_path, category)
            if not dry_run:
                os.makedirs(target_dir, exist_ok=True)
            
            new_name = self.generate_smart_name(original_path, category)
            new_path = os.path.join(target_dir, new_name)
            
            # Handle duplicates
            counter = 1
            while os.path.exists(new_path) and new_path != original_path:
                name, ext = os.path.splitext(new_name)
                new_name = f"{name}_{counter}{ext}"
                new_path = os.path.join(target_dir, new_name)
                counter += 1
            
            try:
                if dry_run:
                    results.append({
                        "original_path": original_path,
                        "new_path": new_path,
                        "action": "Would move"
                    })
                    organized_count += 1
                else:
                    shutil.move(original_path, new_path)
                    results.append({
                        "original_path": original_path,
                        "new_path": new_path,
                        "action": "Moved"
                    })
                    organized_count += 1
            except Exception as e:
                errors.append(f"Failed to move {os.path.basename(original_path)}: {e}")
        
        return organized_count, errors, results
    
    def get_stats(self) -> Dict:
        files = self.scan_files()
        stats = {
            "total_scanned": len(files),
            "total_organized": 0,
            "categories": {cat: 0 for cat in self.categories}
        }
        
        if os.path.exists(self.organized_path):
            for root, dirs, files in os.walk(self.organized_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    category = self.get_category(file_path)
                    if category in stats["categories"]:
                        stats["categories"][category] += 1
                        stats["total_organized"] += 1
        
        return stats

# Create organizer instance (no async issues)
organizer = FileOrganizer()

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

# Files endpoints
@app.get("/api/files")
async def get_files(category: Optional[str] = None, limit: int = 100):
    """Get list of files"""
    files = organizer.scan_files(limit)
    
    if category:
        files = [f for f in files if f["category"].lower() == category.lower()]
    
    return {
        "files": files,
        "total": len(files),
        "limit": limit
    }

@app.post("/api/files/scan")
async def scan_files():
    """Scan files"""
    files = organizer.scan_files()
    return {
        "message": "Scan completed",
        "files_found": len(files),
        "files": files
    }

@app.post("/api/files/organize")
async def organize_files(request: OrganizeRequest):
    """Organize files"""
    organized_count, errors, results = organizer.organize_files(dry_run=request.dry_run)
    
    return {
        "message": "Organization completed" if not request.dry_run else "Dry run completed",
        "organized_count": organized_count,
        "errors": errors,
        "results": results,
        "dry_run": request.dry_run
    }

@app.get("/api/files/stats")
async def get_stats():
    """Get stats"""
    return organizer.get_stats()

# Dashboard endpoints
@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    stats = organizer.get_stats()
    return {
        "total_files": stats["total_scanned"],
        "organized_files": stats["total_organized"],
        "categories": stats["categories"]
    }

@app.get("/api/dashboard/activity")
async def get_recent_activity():
    return {
        "activities": [
            {
                "id": 1,
                "action": "file_organized",
                "file_name": "document.pdf",
                "timestamp": datetime.now().isoformat()
            }
        ]
    }

@app.get("/api/dashboard/folders")
async def get_folder_structure():
    return {
        "folders": [
            {
                "name": "Documents",
                "path": os.path.join(organizer.organized_path, "Documents"),
                "file_count": 0
            }
        ]
    }

@app.get("/api/dashboard/storage")
async def get_storage_info():
    return {
        "total_size": 1000000,
        "organized_size": 0,
        "available_space": 1000000000
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
