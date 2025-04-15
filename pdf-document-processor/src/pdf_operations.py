"""PDF operations for the document processor."""

from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any
from pypdf import PdfWriter, PdfReader


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
    merger = None
    try:
        merger = PdfWriter()
        
        for file_info in files_to_merge:
            path = file_info['path']
            pages = file_info.get('pages')
            desc = file_info.get('description', path.name)
            
            print(f"  Adding: {desc}")
            
            if pages:
                with open(path, "rb") as f:
                    reader = PdfReader(f)
                    if len(reader.pages) > pages[1]:
                        merger.append(fileobj=f, pages=pages)
                    else:
                        print(f"  Warning: {desc} has fewer pages than requested. Skipping.")
            else:
                merger.append(str(path))
        
        print(f"  Saving merged file to: {output_path}")
        merger.write(str(output_path))
        return True
        
    except Exception as e:
        print(f"Error merging PDFs: {e}")
        return False
    finally:
        if merger:
            try:
                merger.close()
            except Exception as e:
                print(f"Error closing PDF writer: {e}")
