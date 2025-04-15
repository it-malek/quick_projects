"""GUI utilities for file and folder selection."""

import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from typing import Optional, List, Tuple


def initialize_tk_root() -> tk.Tk:
    """Initialize and hide the Tkinter root window."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    return root


def select_folder(title: str, initial_dir: str = ".") -> Optional[Path]:
    """Open a folder selection dialog and return the selected path.
    
    Args:
        title: Dialog title
        initial_dir: Initial directory to display
        
    Returns:
        Path object of selected folder or None if cancelled
    """
    root = initialize_tk_root()
    print(f"--> Please select: {title}")
    folder_path = filedialog.askdirectory(title=title, initialdir=initial_dir)
    root.destroy()
    
    if folder_path:
        print(f"    Selected: {folder_path}")
        return Path(folder_path)
    else:
        print("    Selection cancelled.")
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
    root = initialize_tk_root()
    print(f"--> Please select: {title}")
    file_path = filedialog.askopenfilename(
        title=title, 
        filetypes=filetypes,
        initialdir=initial_dir
    )
    root.destroy()
    
    if file_path:
        print(f"    Selected: {file_path}")
        return Path(file_path)
    else:
        print("    Selection cancelled.")
        return None
