"""Configuration module for the PDF Document Processor."""

import dataclasses
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import datetime
import json

logger = logging.getLogger(__name__)

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

    def __post_init__(self):
        """Convert string paths to Path objects if needed."""
        if isinstance(self.source_folder, str):
            self.source_folder = Path(self.source_folder)
        if isinstance(self.supplementary_folder, str) and self.supplementary_folder:
            self.supplementary_folder = Path(self.supplementary_folder)
        if isinstance(self.appendix_file, str) and self.appendix_file:
            self.appendix_file = Path(self.appendix_file)
        if isinstance(self.output_folder, str):
            self.output_folder = Path(self.output_folder)
        if isinstance(self.start_date, str):
            self.start_date = datetime.datetime.strptime(self.start_date, "%Y-%m-%d").date()

    def validate(self) -> bool:
        """Validate the configuration."""
        try:
            if not self.source_folder.exists():
                logger.error(f"Source folder does not exist: {self.source_folder}")
                return False
                
            if self.supplementary_folder and not self.supplementary_folder.exists():
                logger.error(f"Supplementary folder does not exist: {self.supplementary_folder}")
                return False
                
            if self.appendix_file and not self.appendix_file.is_file():
                logger.error(f"Appendix file does not exist: {self.appendix_file}")
                return False
                
            if not self.output_folder.exists():
                logger.info(f"Creating output folder: {self.output_folder}")
                try:
                    self.output_folder.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    logger.error(f"Failed to create output folder: {e}")
                    return False
                    
            return True
        except Exception as e:
            logger.error(f"Error validating configuration: {e}")
            return False
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to a dictionary for serialization."""
        return {
            "source_folder": str(self.source_folder),
            "supplementary_folder": str(self.supplementary_folder) if self.supplementary_folder else None,
            "appendix_file": str(self.appendix_file) if self.appendix_file else None,
            "output_folder": str(self.output_folder),
            "start_date": self.start_date.isoformat(),
            "file_pattern": self.file_pattern,
            "id_pattern": self.id_pattern,
            "recursive": self.recursive
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProcessorConfig':
        """Create config from a dictionary."""
        # Convert date string to date object
        if isinstance(data.get("start_date"), str):
            data["start_date"] = datetime.datetime.strptime(
                data["start_date"], "%Y-%m-%d"
            ).date()
        return cls(**data)
        
    def save_to_file(self, file_path: Path) -> bool:
        """Save configuration to a JSON file."""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)
            logger.info(f"Configuration saved to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False
            
    @classmethod
    def load_from_file(cls, file_path: Path) -> Optional['ProcessorConfig']:
        """Load configuration from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            logger.info(f"Configuration loaded from {file_path}")
            return cls.from_dict(data)
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return None
