"""Core document processing logic."""

import datetime
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .config import ProcessorConfig
from .file_utils import get_file_date, extract_id_from_filename, find_matching_files
from .pdf_operations import merge_pdf_files


class DocumentProcessor:
    """Processor for merging and organizing document files."""
    
    def __init__(self, config: ProcessorConfig):
        """Initialize with configuration.
        
        Args:
            config: ProcessorConfig object with processing parameters
        """
        self.config = config
        self.stats = {
            "processed": 0,
            "skipped_format": 0,
            "skipped_date": 0,
            "errors": 0
        }
    
    def process_documents(self) -> Dict[str, int]:
        """Process all documents according to configuration.
        
        Returns:
            Dictionary with processing statistics
        """
        if not self.config.validate():
            print("Error: Invalid configuration")
            return self.stats
            
        print("\nScanning for documents...")
        source_files = list(self.config.source_folder.glob(self.config.file_pattern))
        
        if not source_files:
            print(f"No matching files found in {self.config.source_folder}")
            return self.stats
            
        print(f"Found {len(source_files)} potential documents. Processing...")
        
        for source_path in source_files:
            if not source_path.is_file():
                continue
                
            # Check file date
            file_date = get_file_date(source_path)
            if file_date and file_date < self.config.start_date:
                self.stats["skipped_date"] += 1
                continue
                
            # Extract ID from filename
            doc_id = extract_id_from_filename(source_path.name, self.config.id_pattern)
            if not doc_id:
                self.stats["skipped_format"] += 1
                continue
                
            # Process this document
            self._process_single_document(source_path, doc_id, file_date)
            
        return self.stats
    
    def _process_single_document(
        self, 
        source_path: Path, 
        doc_id: str, 
        file_date: Optional[datetime.date]
    ) -> None:
        """Process a single document file.
        
        Args:
            source_path: Path to the source document
            doc_id: Extracted document ID
            file_date: Document modification date or None
        """
        date_str = file_date.strftime('%Y-%m-%d') if file_date else "Unknown Date"
        print("-" * 40)
        print(f"Processing: {source_path.name} (Date: {date_str})")
        print(f"  Extracted ID: {doc_id}")
        
        # Find supplementary document if configured
        supp_path = None
        if self.config.supplementary_folder:
            matching_files = find_matching_files(
                self.config.supplementary_folder, 
                doc_id
            )
            if matching_files:
                supp_path = matching_files[0]
                print(f"  Found supplementary file: {supp_path.name}")
                if len(matching_files) > 1:
                    print(f"  Note: Multiple matches found. Using '{supp_path.name}'")
        
        # Define output path
        output_path = self.config.output_folder / source_path.name
        
        # Prepare files to merge
        files_to_merge = [
            {"path": source_path, "description": f"Main document: {source_path.name}"}
        ]
        
        # Add supplementary document if found
        if supp_path and supp_path.is_file():
            try:
                # Add all pages except the last one
                files_to_merge.append({
                    "path": supp_path,
                    "pages": (0, -2),  # All pages except the last
                    "description": f"Supplementary data: {supp_path.name} (excluding last page)"
                })
            except Exception as e:
                print(f"  Error preparing supplementary file: {e}")
        
        # Add appendix if configured
        if self.config.appendix_file and self.config.appendix_file.is_file():
            files_to_merge.append({
                "path": self.config.appendix_file,
                "description": f"Appendix: {self.config.appendix_file.name}"
            })
        
        # Perform the merge
        success = merge_pdf_files(files_to_merge, output_path)
        
        if success:
            print(f"  Successfully merged and saved to {output_path}")
            self.stats["processed"] += 1
        else:
            print(f"  Failed to process {source_path.name}")
            self.stats["errors"] += 1
