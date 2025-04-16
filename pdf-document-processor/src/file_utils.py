"""File utility functions for the PDF Document Processor."""

import os
import re
import logging
import datetime
from pathlib import Path
from typing import Optional, List, Pattern, Dict, Any

logger = logging.getLogger(__name__)

def get_file_date(file_path: Path) -> Optional[datetime.date]:
    """Get the modification date of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Date of last modification or None if error
    """
    try:
        if not file_path.exists():
            logger.warning(f"File does not exist: {file_path}")
            return None
            
        file_mtime_ts = os.path.getmtime(file_path)
        return datetime.date.fromtimestamp(file_mtime_ts)
    except Exception as e:
        logger.warning(f"Could not get date for {file_path.name}: {e}")
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
        if not filename:
            return None
            
        clean_filename = filename.strip()
        parts = clean_filename.split(" ", 1)
        if parts:
            potential_id = parts[0].strip()
            if re.match(pattern, potential_id, re.IGNORECASE):
                logger.debug(f"Extracted ID '{potential_id}' from '{filename}'")
                return potential_id
                
        logger.debug(f"No ID matching pattern '{pattern}' found in '{filename}'")
        return None
    except Exception as e:
        logger.error(f"Error extracting ID from filename '{filename}': {e}")
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
        if not folder or not folder.exists():
            logger.warning(f"Folder does not exist: {folder}")
            return []
            
        if not id_value:
            logger.warning("Empty ID value provided")
            return []
            
        pattern = f"{re.escape(id_value)} *{extension}"
        logger.debug(f"Searching for files matching pattern '{pattern}' in {folder}")
        
        matching_files = list(folder.glob(pattern))
        matching_files.sort()
        
        logger.info(f"Found {len(matching_files)} files matching ID '{id_value}'")
        return matching_files
    except Exception as e:
        logger.error(f"Error searching for files matching '{id_value}': {e}")
        print(f"Error searching for files matching '{id_value}': {e}")
        return []
