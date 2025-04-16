"""PDF operations for the document processor."""

import logging
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any
from pypdf import PdfWriter, PdfReader

logger = logging.getLogger(__name__)

def merge_pdf_files(
    files_to_merge: List[Dict[str, Any]], 
    output_path: Path
) -> bool:
    """Merge multiple PDF files into a single output file.
    
    Args:
        files_to_merge: List of dicts with file info:
            {
                'path': Path object,
                'pages': Optional tuple of (start, end) pages or None for all
                'description': String description for logging
            }
        output_path: Path where to save the merged PDF
        
    Returns:
        True if successful, False otherwise
    """
    if not files_to_merge:
        logger.error("No files provided to merge")
        return False
        
    merger = None
    try:
        merger = PdfWriter()
        
        for file_info in files_to_merge:
            path = file_info['path']
            pages = file_info.get('pages')
            desc = file_info.get('description', path.name)
            
            logger.info(f"Adding: {desc}")
            print(f"  Adding: {desc}")
            
            if not path.exists():
                logger.warning(f"File does not exist: {path}")
                print(f"  Warning: File does not exist: {path}. Skipping.")
                continue
                
            if pages:
                with open(path, "rb") as f:
                    reader = PdfReader(f)
                    total_pages = len(reader.pages)
                    
                    # Handle negative indices for end page
                    start_page, end_page = pages
                    if end_page < 0:
                        end_page = total_pages + end_page
                        
                    if total_pages > 0:
                        if end_page >= total_pages:
                            logger.warning(f"{desc} has {total_pages} pages, requested up to {end_page}")
                            print(f"  Warning: {desc} has fewer pages than requested. Using all available pages.")
                            merger.append(fileobj=f, pages=(start_page, total_pages-1))
                        else:
                            merger.append(fileobj=f, pages=pages)
                    else:
                        logger.warning(f"{desc} has no pages")
                        print(f"  Warning: {desc} has no pages. Skipping.")
            else:
                merger.append(str(path))
        
        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Saving merged file to: {output_path}")
        print(f"  Saving merged file to: {output_path}")
        merger.write(str(output_path))
        return True
        
    except Exception as e:
        logger.error(f"Error merging PDFs: {e}", exc_info=True)
        print(f"Error merging PDFs: {e}")
        return False
    finally:
        if merger:
            try:
                merger.close()
            except Exception as e:
                logger.error(f"Error closing PDF writer: {e}")
                print(f"Error closing PDF writer: {e}")
        # else:
        #     logger.warning("Merger was never initialized")
        #     print("Warning: Merger was never initialized")