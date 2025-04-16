#!/usr/bin/env python3
"""
PDF Document Processor

A tool for merging and organizing PDF documents with supplementary data
and appendices based on document IDs and dates.
"""

import argparse
import datetime
import logging
import sys
from pathlib import Path

from src.config import ProcessorConfig
from src.document_processor import DocumentProcessor
from src.gui_utils import select_folder, select_file


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def parse_date(date_str: str) -> datetime.date:
    """Parse a date string in YYYY-MM-DD format."""
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        logger.warning(f"Invalid date format: {date_str}. Using today's date instead.")
        return datetime.date.today()


def get_user_input_date() -> datetime.date:
    """Prompt user for a date with today as default."""
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    date_str = input(
        f"Enter start date (YYYY-MM-DD) to process files "
        f"[leave blank for today: {today_str}]: "
    ).strip()
    return parse_date(date_str) if date_str else datetime.date.today()


def interactive_setup() -> ProcessorConfig:
    """Set up configuration interactively using GUI dialogs."""
    logger.info("Starting interactive configuration")
    print("--- PDF Document Processor Configuration ---")
    
    # Get source folder
    source_folder = select_folder("Select the Folder Containing Source PDFs")
    if not source_folder:
        logger.error("No source folder selected")
        print("Error: No source folder selected. Exiting.")
        sys.exit(1)
    
    # Get supplementary folder
    supp_folder = select_folder("Select the Folder Containing Supplementary PDFs (optional)")
    
    # Get appendix file
    appendix_file = select_file(
        "Select the Appendix PDF File (optional)", 
        [("PDF files", "*.pdf")]
    )
    
    # Get output folder
    output_folder = select_folder("Select the OUTPUT Folder for Processed Files")
    if not output_folder:
        logger.error("No output folder selected")
        print("Error: No output folder selected. Exiting.")
        sys.exit(1)
    
    # Get start date via console
    start_date = get_user_input_date()
    
    # Create and return config
    config = ProcessorConfig(
        source_folder=source_folder,
        supplementary_folder=supp_folder,
        appendix_file=appendix_file,
        output_folder=output_folder,
        start_date=start_date
    )
    
    print("\n--- Configuration Summary ---")
    print(f"Source Folder:        {config.source_folder}")
    print(f"Supplementary Folder: {config.supplementary_folder or 'None'}")
    print(f"Appendix File:        {config.appendix_file or 'None'}")
    print(f"Output Folder:        {config.output_folder}")
    print(f"Process from date:    {config.start_date.strftime('%Y-%m-%d')}")
    print("-----------------------------")
    
    logger.info("Configuration completed successfully")
    return config


def batch_setup(args) -> ProcessorConfig:
    """Set up configuration from command line arguments."""
    # This is a placeholder for future batch mode implementation
    logger.error("Batch mode not implemented yet")
    raise NotImplementedError("Batch mode not yet implemented")


def main():
    """Main entry point for the PDF Document Processor."""
    parser = argparse.ArgumentParser(description="PDF Document Processor")
    parser.add_argument(
        "--batch", action="store_true", 
        help="Run in batch mode with command line arguments"
    )
    parser.add_argument(
        "--source", type=str,
        help="Source folder containing PDF files (for batch mode)"
    )
    parser.add_argument(
        "--output", type=str,
        help="Output folder for processed files (for batch mode)"
    )
    parser.add_argument(
        "--supplementary", type=str,
        help="Folder containing supplementary PDFs (for batch mode)"
    )
    parser.add_argument(
        "--appendix", type=str,
        help="Path to appendix PDF file (for batch mode)"
    )
    parser.add_argument(
        "--date", type=str,
        help="Start date in YYYY-MM-DD format (for batch mode)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Set logging level based on verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    
    try:
        if args.batch:
            # Implement batch mode configuration here
            logger.info("Starting in batch mode")
            try:
                config = batch_setup(args)
            except NotImplementedError as e:
                print(f"Error: {e}")
                sys.exit(1)
        else:
            # Interactive mode
            logger.info("Starting in interactive mode")
            config = interactive_setup()
        
        # Process documents
        logger.info("Beginning document processing")
        processor = DocumentProcessor(config)
        stats = processor.process_documents()
        
        # Print results
        print("\n--- Processing Results ---")
        print(f"Successfully Processed: {stats['processed']}")
        print(f"Skipped (Invalid Format): {stats['skipped_format']}")
        print(f"Skipped (Before Date): {stats['skipped_date']}")
        print(f"Errors: {stats['errors']}")
        print("-------------------------")
        
        logger.info(f"Processing completed. Processed: {stats['processed']}, Errors: {stats['errors']}")
        return 0
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
