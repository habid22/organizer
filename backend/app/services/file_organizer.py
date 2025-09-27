"""
File organization service for intelligent file categorization and naming.
"""

import os
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import magic
from PIL import Image
import PyPDF2

from app.core.config import settings
from app.models.file import File
from app.models.organization_rule import OrganizationRule

class FileOrganizerService:
    """Service for organizing and categorizing files"""
    
    def __init__(self):
        self.supported_extensions = settings.supported_extensions
        self.default_categories = settings.default_categories
    
    def organize_file(self, file_path: str) -> Dict:
        """
        Organize a single file based on its type and content.
        
        Args:
            file_path: Path to the file to organize
            
        Returns:
            Dict with organization results
        """
        try:
            # Get file information
            file_info = self._get_file_info(file_path)
            
            # Determine category
            category = self._determine_category(file_path, file_info)
            
            # Generate new name
            new_name = self._generate_smart_name(file_path, file_info, category)
            
            # Determine target folder
            target_folder = self._get_target_folder(category)
            
            # Create target directory if it doesn't exist
            os.makedirs(target_folder, exist_ok=True)
            
            # Generate new path
            new_path = os.path.join(target_folder, new_name)
            
            # Handle duplicates
            new_path = self._handle_duplicates(new_path)
            
            # Move file
            shutil.move(file_path, new_path)
            
            return {
                "success": True,
                "original_path": file_path,
                "new_path": new_path,
                "category": category,
                "new_name": new_name,
                "file_info": file_info
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "original_path": file_path
            }
    
    def _get_file_info(self, file_path: str) -> Dict:
        """Extract file information and metadata"""
        stat = os.stat(file_path)
        
        # Get MIME type
        mime_type = magic.from_file(file_path, mime=True)
        
        # Get file extension
        file_ext = Path(file_path).suffix.lower()
        
        # Calculate checksum for duplicate detection
        checksum = self._calculate_checksum(file_path)
        
        return {
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime),
            "modified": datetime.fromtimestamp(stat.st_mtime),
            "mime_type": mime_type,
            "extension": file_ext,
            "checksum": checksum
        }
    
    def _determine_category(self, file_path: str, file_info: Dict) -> str:
        """Determine the category for a file"""
        file_ext = file_info["extension"]
        
        # Check against default categories
        for category, extensions in self.default_categories.items():
            if file_ext in extensions:
                return category
        
        # Default to "other" if no category matches
        return "other"
    
    def _generate_smart_name(self, file_path: str, file_info: Dict, category: str) -> str:
        """Generate a smart name for the file"""
        original_name = Path(file_path).name
        file_ext = file_info["extension"]
        created_time = file_info["created"]
        
        # Generate timestamp
        timestamp = created_time.strftime("%Y-%m-%d_%H-%M")
        
        # Handle different file types
        if category == "images":
            if "screenshot" in original_name.lower():
                return f"screenshot_{timestamp}{file_ext}"
            else:
                return f"image_{timestamp}{file_ext}"
        
        elif category == "documents":
            # Try to extract meaningful name from content
            if "invoice" in original_name.lower():
                return f"invoice_{timestamp}{file_ext}"
            elif "report" in original_name.lower():
                return f"report_{timestamp}{file_ext}"
            else:
                return f"document_{timestamp}{file_ext}"
        
        elif category == "software":
            return f"software_{timestamp}{file_ext}"
        
        elif category == "archives":
            return f"archive_{timestamp}{file_ext}"
        
        else:
            # Default naming pattern
            return f"file_{timestamp}{file_ext}"
    
    def _get_target_folder(self, category: str) -> str:
        """Get the target folder for a category"""
        base_path = settings.downloads_path
        category_folder = os.path.join(base_path, category.title())
        
        # Add year-month subfolder
        now = datetime.now()
        year_month = now.strftime("%Y-%m")
        return os.path.join(category_folder, year_month)
    
    def _handle_duplicates(self, target_path: str) -> str:
        """Handle duplicate file names"""
        if not os.path.exists(target_path):
            return target_path
        
        # Add number suffix
        base_path = Path(target_path)
        counter = 1
        
        while True:
            new_name = f"{base_path.stem}_{counter}{base_path.suffix}"
            new_path = base_path.parent / new_name
            
            if not os.path.exists(new_path):
                return str(new_path)
            
            counter += 1
    
    def _calculate_checksum(self, file_path: str) -> str:
        """Calculate MD5 checksum for duplicate detection"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def detect_duplicates(self, file_paths: List[str]) -> List[Dict]:
        """Detect duplicate files based on content"""
        checksums = {}
        duplicates = []
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                checksum = self._calculate_checksum(file_path)
                
                if checksum in checksums:
                    duplicates.append({
                        "original": checksums[checksum],
                        "duplicate": file_path,
                        "checksum": checksum
                    })
                else:
                    checksums[checksum] = file_path
        
        return duplicates
