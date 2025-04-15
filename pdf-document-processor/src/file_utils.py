"""File utility functions for the PDF Document Processor."""

import os
import re
import datetime
from pathlib import Path
from typing import Optional, List, Pattern, Dict, Any


def get_file_date(file_path: Path) -> Optional[datetime.date]:
    """Get the modification date of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Date of last modification or None if error
    """
    try:
        file_mtime_ts = os.path.getmtime(file_path)
        return datetime.date.fromtimestamp(file_mtime_ts)
    except Exception as e:
        print(f"Warning: Could not get date for {file_path.name}. Error: {e}")
        return None


def extract_id_from_filename(
    filename: str, 
    pattern: str = r"^[A-Za-z]\d+$"
) -> Optional[str]:
    """Extract an ID from a filename based on a regex pattern.
    
    Args:
        filename: Filename to extract ID from
        pattern: Regex pattern for the ID
        
    Returns:
        Extracted ID or None if not found
    """
    try:
        clean_filename = filename.strip()
        parts = clean_filename.split(" ", 1)
        if parts:
            potential_id = parts[0].strip()
            if re.match(pattern, potential_id, re.IGNORECASE):
                return potential_id
        return None
    except Exception as e:
        print(f"Error extracting ID from filename '{filename}': {e}")
        return None


def find_matching_files(
    folder: Path, 
    id_value: str, 
    extension: str = ".pdf"
) -> List[Path]:
    """Find files in a folder matching an ID pattern.
    
    Args:
        folder: Folder to search in
        id_value: ID to match at the start of filenames
        extension: File extension to filter by
        
    Returns:
        List of matching file paths
    """
    try:
        pattern = f"{re.escape(id_value)} *{extension}"
        matching_files = list(folder.glob(pattern))
        matching_files.sort()
        return matching_files
    except Exception as e:
        print(f"Error searching for files matching '{id_value}': {e}")
        return []
