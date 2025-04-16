"""Core document processing logic."""

import datetime
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .config import ProcessorConfig
from .file_utils import get_file_date, extract_id_from_filename, find_matching_files
from .pdf_operations import merge_pdf_files

logger = logging.getLogger(__name__)

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
        logger.info("Document processor initialized")
    
    def process_documents(self) -> Dict[str, int]:
        """Process all documents according to configuration.
        
        Returns:
            Dictionary with processing statistics
        """
        if not self.config.validate():
            logger.error("Invalid configuration")
            print("Error: Invalid configuration")
            return self.stats
            
        logger.info(f"Scanning for documents in {self.config.source_folder}")
        print("\nScanning for documents...")
        
        # Use recursive glob if configured
        if self.config.recursive:
            glob_pattern = f"**/{self.config.file_pattern}"
        else:
            glob_pattern = self.config.file_pattern
            
        source_files = list(self.config.source_folder.glob(glob_pattern))
        
        if not source_files:
            logger.warning(f"No matching files found in {self.config.source_folder}")
            print(f"No matching files found in {self.config.source_folder}")
            return self.stats
            
        logger.info(f"Found {len(source_files)} potential documents")
        print(f"Found {len(source_files)} potential documents. Processing...")
        
        for source_path in source_files:
            if not source_path.is_file():
                logger.debug(f"Skipping non-file: {source_path}")
                continue
                
            # Check file date
            file_date = get_file_date(source_path)
            if file_date and file_date < self.config.start_date:
                logger.debug(f"Skipping {source_path.name} - before start date")
                self.stats["skipped_date"] += 1
                continue
                
            # Extract ID from filename
            doc_id = extract_id_from_filename(source_path.name, self.config.id_pattern)
            if not doc_id:
                logger.debug(f"Skipping {source_path.name} - no valid ID found")
                self.stats["skipped_format"] += 1
                continue
                
            # Process this document
            self._process_single_document(source_path, doc_id, file_date)
            
        logger.info(f"Processing complete. Stats: {self.stats}")
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
        logger.info(f"Processing document: {source_path.name} (ID: {doc_id}, Date: {date_str})")
        
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
                logger.info(f"Found supplementary file: {supp_path.name}")
                print(f"  Found supplementary file: {supp_path.name}")
                if len(matching_files) > 1:
                    logger.warning(f"Multiple matches found for ID {doc_id}. Using '{supp_path.name}'")
                    print(f"  Note: Multiple matches found. Using '{supp_path.name}'")
            else:
                logger.info(f"No supplementary file found for ID {doc_id}")
        
        # Define output path
        output_path = self.config.output_folder / source_path.name
        
        # Check if output file already exists
        if output_path.exists():
            logger.warning(f"Output file already exists: {output_path}")
            print(f"  Warning: Output file already exists. It will be overwritten.")
        
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
                logger.error(f"Error preparing supplementary file: {e}")
                print(f"  Error preparing supplementary file: {e}")
                self.stats["errors"] += 1
        
        # Add appendix if configured
        if self.config.appendix_file and self.config.appendix_file.is_file():
            files_to_merge.append({
                "path": self.config.appendix_file,
                "description": f"Appendix: {self.config.appendix_file.name}"
            })
        
        # Perform the merge
        success = merge_pdf_files(files_to_merge, output_path)
        
        if success:
            logger.info(f"Successfully processed {source_path.name}")
            print(f"  Successfully merged and saved to {output_path}")
            self.stats["processed"] += 1
        else:
            logger.error(f"Failed to process {source_path.name}")
            print(f"  Failed to process {source_path.name}")
            self.stats["errors"] += 1
