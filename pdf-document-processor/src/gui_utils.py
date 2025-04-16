"""GUI utilities for file and folder selection."""

import logging
import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from typing import Optional, List, Tuple

logger = logging.getLogger(__name__)

def initialize_tk_root() -> tk.Tk:
    """Initialize and hide the Tkinter root window."""
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Make it nicer on macOS
        if hasattr(root, 'tk'):
            root.tk.call('::tk::unsupported::MacWindowStyle', 'style', root._w, 'plain', 'none')
        
        return root
    except Exception as e:
        logger.error(f"Failed to initialize Tkinter: {e}", exc_info=True)
        raise


def select_folder(title: str, initial_dir: str = ".") -> Optional[Path]:
    """Open a folder selection dialog and return the selected path.
    
    Args:
        title: Dialog title
        initial_dir: Initial directory to display
        
    Returns:
        Path object of selected folder or None if cancelled
    """
    # Ensure initial_dir exists and is absolute
    if not os.path.exists(initial_dir):
        initial_dir = os.path.expanduser("~")
    initial_dir = os.path.abspath(initial_dir)
    
    logger.debug(f"Opening folder selection dialog: {title}")
    print(f"--> Please select: {title}")
    
    try:
        root = initialize_tk_root()
        folder_path = filedialog.askdirectory(title=title, initialdir=initial_dir)
        root.destroy()
        
        if folder_path:
            logger.info(f"Selected folder: {folder_path}")
            print(f"    Selected: {folder_path}")
            return Path(folder_path)
        else:
            logger.info("Folder selection cancelled")
            print("    Selection cancelled.")
            return None
    except Exception as e:
        logger.error(f"Error in folder selection: {e}", exc_info=True)
        print(f"    Error in folder selection: {e}")
        return None


def select_file(
    title: str, 
    filetypes: List[Tuple[str, str]], 
    initial_dir: str = "."
) -> Optional[Path]:
    """Open a file selection dialog and return the selected path.
    
    Args:
        title: Dialog title
        filetypes: List of file type tuples (description, pattern)
        initial_dir: Initial directory to display
        
    Returns:
        Path object of selected file or None if cancelled
    """
    # Ensure initial_dir exists and is absolute
    if not os.path.exists(initial_dir):
        initial_dir = os.path.expanduser("~")
    initial_dir = os.path.abspath(initial_dir)
    
    logger.debug(f"Opening file selection dialog: {title}")
    print(f"--> Please select: {title}")
    
    try:
        root = initialize_tk_root()
        file_path = filedialog.askopenfilename(
            title=title, 
            filetypes=filetypes,
            initialdir=initial_dir
        )
        root.destroy()
        
        if file_path:
            logger.info(f"Selected file: {file_path}")
            print(f"    Selected: {file_path}")
            return Path(file_path)
        else:
            logger.info("File selection cancelled")
            print("    Selection cancelled.")
            return None
    except Exception as e:
        logger.error(f"Error in file selection: {e}", exc_info=True)
        print(f"    Error in file selection: {e}")
        return None
