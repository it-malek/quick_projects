"""
PDF Document Processor - A utility for merging and organizing PDF documents.

This package provides tools for merging PDF files, extracting document IDs,
and organizing documents based on date and other criteria.
"""

import logging

# Set up a null handler to avoid "No handler found" warnings
logging.getLogger(__name__).addHandler(logging.NullHandler())

__version__ = "0.1.0"
__author__ = "Malek Elaghel"
__email__ = "malekelaghel@gmail.com"
__license__ = "MIT"
# __status__ = "Development"
# __all__ = [
#     "DocumentProcessor",
#     "FileUtils",
#     "GUIUtils",
#     "Config",
# ]
# from .document_processor import DocumentProcessor
# from .file_utils import FileUtils
# from .gui_utils import GUIUtils
# from .config import ProcessorConfig
# from .exceptions import ProcessorError
