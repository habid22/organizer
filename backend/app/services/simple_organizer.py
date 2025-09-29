"""
Simple Downloads Organizer Service
Based on the working simple_organizer.py script
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

class SimpleOrganizerService:
    """Simple file organizer service that actually works"""
    
    def __init__(self, downloads_path: str = None):
        if downloads_path:
            self.downloads_path = downloads_path
        else:
            # Use cross-platform detection
            import os
            self.downloads_path = os.path.expanduser("~/Downloads")
        self.organized_path = os.path.join(self.downloads_path, "Organized")
        
        # File categories
        self.categories = {
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
        
        # Create organized folder structure
        self._create_folders()
    
    def _create_folders(self):
        """Create organized folder structure"""
        for category in self.categories.keys():
            category_path = os.path.join(self.organized_path, category)
            os.makedirs(category_path, exist_ok=True)
    
    def _get_category(self, file_path: str) -> str:
        """Determine file category based on extension"""
        file_ext = Path(file_path).suffix.lower()
        
        for category, extensions in self.categories.items():
            if file_ext in extensions:
                return category
        
        return "Other"
    
    def _generate_smart_name(self, file_path: str, category: str) -> str:
        """Generate a smart name for the file"""
        original_name = Path(file_path).name
        file_ext = Path(file_path).suffix
        created_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        # Generate timestamp
        timestamp = created_time.strftime("%Y-%m-%d_%H-%M")
        
        # Handle different file types
        if category == "Images":
            if "screenshot" in original_name.lower():
                return f"screenshot_{timestamp}{file_ext}"
            elif "image" in original_name.lower():
                return f"image_{timestamp}{file_ext}"
            else:
                return f"photo_{timestamp}{file_ext}"
        
        elif category == "Documents":
            if "invoice" in original_name.lower():
                return f"invoice_{timestamp}{file_ext}"
            elif "report" in original_name.lower():
                return f"report_{timestamp}{file_ext}"
            else:
                return f"document_{timestamp}{file_ext}"
        
        elif category == "Software":
            return f"software_{timestamp}{file_ext}"
        
        elif category == "Archives":
            return f"archive_{timestamp}{file_ext}"
        
        else:
            # Default naming pattern
            return f"file_{timestamp}{file_ext}"
    
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
    
    def scan_files(self, max_files: int = 100) -> List[Dict]:
        """Scan downloads folder and return file information"""
        files_found = []
        
        if not os.path.exists(self.downloads_path):
            return files_found
        
        # Only scan the top level of downloads folder for performance
        try:
            files = os.listdir(self.downloads_path)
            for file in files[:max_files]:  # Limit to max_files for performance
                file_path = os.path.join(self.downloads_path, file)
                
                # Skip directories and the Organized folder
                if os.path.isdir(file_path) or "Organized" in file_path:
                    continue
                
                try:
                    category = self._get_category(file_path)
                    file_size = os.path.getsize(file_path)
                    created_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    files_found.append({
                        "name": file,
                        "path": file_path,
                        "category": category,
                        "size": file_size,
                        "size_mb": round(file_size / (1024 * 1024), 2),
                        "created": created_time.isoformat(),
                        "extension": Path(file_path).suffix.lower()
                    })
                except (OSError, IOError):
                    # Skip files that can't be accessed
                    continue
        except (OSError, IOError):
            # Skip if downloads folder can't be accessed
            pass
        
        return files_found
    
    def organize_files(self, dry_run: bool = True) -> Tuple[int, List[str]]:
        """Organize files into categories"""
        organized_count = 0
        errors = []
        results = []
        
        for root, dirs, files in os.walk(self.downloads_path):
            # Skip the organized folder
            if "Organized" in root:
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    # Get category
                    category = self._get_category(file_path)
                    
                    # Generate new name
                    new_name = self._generate_smart_name(file_path, category)
                    
                    # Create target path
                    target_folder = os.path.join(self.organized_path, category)
                    target_path = os.path.join(target_folder, new_name)
                    
                    # Handle duplicates
                    target_path = self._handle_duplicates(target_path)
                    
                    result = {
                        "original_name": file,
                        "new_name": new_name,
                        "category": category,
                        "original_path": file_path,
                        "new_path": target_path,
                        "success": True
                    }
                    
                    if not dry_run:
                        # Move file
                        shutil.move(file_path, target_path)
                        result["moved"] = True
                    else:
                        result["moved"] = False
                    
                    results.append(result)
                    organized_count += 1
                    
                except Exception as e:
                    error_msg = f"Error with {file}: {str(e)}"
                    errors.append(error_msg)
                    results.append({
                        "original_name": file,
                        "original_path": file_path,
                        "success": False,
                        "error": str(e)
                    })
        
        return organized_count, errors, results
    
    def get_stats(self) -> Dict:
        """Get current organization statistics"""
        stats = {
            "downloads_path": self.downloads_path,
            "organized_path": self.organized_path,
            "categories": {}
        }
        
        for category in self.categories.keys():
            category_path = os.path.join(self.organized_path, category)
            if os.path.exists(category_path):
                try:
                    files = os.listdir(category_path)
                    stats["categories"][category] = len(files)
                except (OSError, IOError):
                    stats["categories"][category] = 0
            else:
                stats["categories"][category] = 0
        
        return stats
