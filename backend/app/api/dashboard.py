"""
API routes for dashboard and statistics.
"""

from fastapi import APIRouter
from app.services.simple_organizer import SimpleOrganizerService

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    organizer = SimpleOrganizerService()
    files = organizer.scan_files()
    stats = organizer.get_stats()
    
    # Calculate totals
    total_files = len(files)
    total_size = sum(f["size"] for f in files)
    
    # Files by category
    category_stats = {}
    for file in files:
        category = file["category"]
        if category not in category_stats:
            category_stats[category] = 0
        category_stats[category] += 1
    
    return {
        "total_files": total_files,
        "category_stats": [{"category": cat, "count": count} for cat, count in category_stats.items()],
        "recent_files": total_files,  # All files are "recent" since we're scanning live
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "duplicate_count": 0,  # Not implemented in simple version
        "organized_stats": stats["categories"]
    }

@router.get("/activity")
async def get_recent_activity(limit: int = 20):
    """Get recent file organization activity"""
    organizer = SimpleOrganizerService()
    files = organizer.scan_files()
    
    # Sort by creation time and limit
    files.sort(key=lambda x: x["created"], reverse=True)
    recent_files = files[:limit]
    
    return {
        "recent_activity": [
            {
                "id": i,
                "original_name": file["name"],
                "new_name": file["name"],  # No renaming in simple version
                "category": file["category"],
                "created_at": file["created"],
                "is_organized": False  # Not organized yet
            }
            for i, file in enumerate(recent_files)
        ]
    }

@router.get("/folders")
async def get_folder_structure():
    """Get current folder structure of downloads"""
    organizer = SimpleOrganizerService()
    stats = organizer.get_stats()
    
    return {
        "folders": [
            {
                "name": category,
                "path": f"{organizer.organized_path}/{category}",
                "file_count": count
            }
            for category, count in stats["categories"].items()
        ],
        "total_files": sum(stats["categories"].values())
    }

@router.get("/storage")
async def get_storage_info():
    """Get storage usage information"""
    organizer = SimpleOrganizerService()
    files = organizer.scan_files()
    
    total_size = sum(f["size"] for f in files)
    file_count = len(files)
    
    return {
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "total_size_gb": round(total_size / (1024 * 1024 * 1024), 2),
        "file_count": file_count
    }
