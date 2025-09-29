#!/usr/bin/env python3
"""
Simple Downloads Organizer - Standalone Script
No database, no API, just works!
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
import json

class SimpleOrganizer:
    def __init__(self, downloads_path=None):
        if downloads_path:
            self.downloads_path = downloads_path
        else:
            # Use cross-platform detection
            self.downloads_path = os.path.expanduser("~/Downloads")
        self.organized_path = os.path.join(self.downloads_path, "Organized")
        
        # Create organized folder structure
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
            print(f"📁 Created folder: {category_path}")
    
    def _get_category(self, file_path):
        """Determine file category based on extension"""
        file_ext = Path(file_path).suffix.lower()
        
        for category, extensions in self.categories.items():
            if file_ext in extensions:
                return category
        
        return "Other"
    
    def _generate_smart_name(self, file_path, category):
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
    
    def _handle_duplicates(self, target_path):
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
    
    def scan_files(self):
        """Scan downloads folder and show what would be organized"""
        print(f"🔍 Scanning: {self.downloads_path}")
        
        files_found = []
        
        for root, dirs, files in os.walk(self.downloads_path):
            # Skip the organized folder
            if "Organized" in root:
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                category = self._get_category(file_path)
                
                files_found.append({
                    "path": file_path,
                    "name": file,
                    "category": category,
                    "size": os.path.getsize(file_path)
                })
        
        return files_found
    
    def organize_files(self, dry_run=True):
        """Organize files into categories"""
        print(f"🗂️  Organizing files in: {self.downloads_path}")
        
        organized_count = 0
        errors = []
        
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
                    
                    if dry_run:
                        print(f"📄 {file} → {category}/{new_name}")
                    else:
                        # Move file
                        shutil.move(file_path, target_path)
                        print(f"✅ Moved: {file} → {category}/{new_name}")
                    
                    organized_count += 1
                    
                except Exception as e:
                    error_msg = f"❌ Error with {file}: {str(e)}"
                    print(error_msg)
                    errors.append(error_msg)
        
        print(f"\n📊 Summary:")
        print(f"   Files organized: {organized_count}")
        print(f"   Errors: {len(errors)}")
        
        return organized_count, errors
    
    def show_stats(self):
        """Show current organization stats"""
        print(f"\n📊 Current Organization Stats:")
        print(f"   Downloads folder: {self.downloads_path}")
        print(f"   Organized folder: {self.organized_path}")
        
        for category in self.categories.keys():
            category_path = os.path.join(self.organized_path, category)
            if os.path.exists(category_path):
                files = os.listdir(category_path)
                print(f"   {category}: {len(files)} files")

def main():
    print("🚀 Simple Downloads Organizer")
    print("=" * 50)
    
    # Initialize organizer
    organizer = SimpleOrganizer()
    
    while True:
        print("\n📋 Options:")
        print("1. Scan files (show what would be organized)")
        print("2. Organize files (DRY RUN - show what would happen)")
        print("3. Organize files (ACTUAL - move files)")
        print("4. Show stats")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            files = organizer.scan_files()
            print(f"\n🔍 Found {len(files)} files to organize:")
            for file_info in files[:10]:  # Show first 10
                print(f"   {file_info['name']} → {file_info['category']}")
            if len(files) > 10:
                print(f"   ... and {len(files) - 10} more files")
        
        elif choice == "2":
            print("\n🔍 DRY RUN - No files will be moved:")
            organizer.organize_files(dry_run=True)
        
        elif choice == "3":
            confirm = input("\n⚠️  This will MOVE files. Continue? (y/N): ").strip().lower()
            if confirm == 'y':
                organizer.organize_files(dry_run=False)
            else:
                print("❌ Cancelled")
        
        elif choice == "4":
            organizer.show_stats()
        
        elif choice == "5":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
