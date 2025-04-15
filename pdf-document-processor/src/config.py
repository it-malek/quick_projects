"""Configuration module for the PDF Document Processor."""

import dataclasses
from pathlib import Path
from typing import Optional
import datetime


@dataclasses.dataclass
class ProcessorConfig:
    """Configuration for the PDF Document Processor."""
    source_folder: Path
    supplementary_folder: Optional[Path]
    appendix_file: Optional[Path]
    output_folder: Path
    start_date: datetime.date
    file_pattern: str = "*.pdf"
    id_pattern: str = r"^[A-Za-z]\d+$"
    recursive: bool = False

    def validate(self) -> bool:
        """Validate the configuration."""
        if not self.source_folder.exists():
            return False
        if self.supplementary_folder and not self.supplementary_folder.exists():
            return False
        if self.appendix_file and not self.appendix_file.is_file():
            return False
        if not self.output_folder.exists():
            try:
                self.output_folder.mkdir(parents=True, exist_ok=True)
            except Exception:
                return False
        return True
