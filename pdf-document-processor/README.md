# PDF Document Processor

A Python utility for merging and organizing PDF documents with supplementary data and appendices. This tool helps automate the process of combining related PDF files based on document IDs and adding standard appendix pages.

## Features

- Merge multiple PDF documents based on document IDs
- Add supplementary data files to main documents
- Append standard ending pages to all documents
- Filter documents by date
- Interactive GUI for file/folder selection
- Detailed processing logs and statistics


## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)


### Install from Source

```
# Clone the repository
git clone https://github.com/yourusername/pdf-document-processor.git
cd pdf-document-processor

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```


## Usage

### Interactive Mode

Run the main script to start the interactive mode:

```
python main.py
```

The application will guide you through:

1. Selecting a source document folder
2. Selecting a supplementary data folder (optional)
3. Selecting an appendix PDF file (optional)
4. Selecting an output folder
5. Entering a start date for processing

### Programmatic Usage

You can also use the package programmatically in your own Python scripts:

```
from pdf_document_processor import ProcessorConfig, DocumentProcessor

# Create a configuration
config = ProcessorConfig(
    source_folder="/path/to/source",
    supplementary_folder="/path/to/supplementary",
    appendix_file="/path/to/appendix.pdf",
    output_folder="/path/to/output",
    start_date="2025-04-01"
)

# Initialize and run the processor
processor = DocumentProcessor(config)
stats = processor.process_documents()

# Print results
print(f"Processed: {stats['processed']}")
print(f"Errors: {stats['errors']}")
```


## Project Structure

```
pdf-document-processor/
├── src/
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Configuration handling
│   ├── document_processor.py # Core processing logic
│   ├── file_utils.py         # File operations and helpers
│   ├── gui_utils.py          # GUI dialog functions
│   └── pdf_operations.py     # PDF-specific operations
├── tests/                    # Unit tests
├── examples/                 # Example usage scripts
├── README.md                 # This file
├── requirements.txt          # Package dependencies
├── setup.py                  # Package installation script
└── main.py                   # Entry point script
```


## Dependencies

- pypdf: PDF manipulation library
- tkinter: GUI toolkit (included with Python)


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the pypdf project for providing the PDF manipulation capabilities
- Inspired by the need to automate repetitive document processing tasks


## Contact

Malek Elaghel - malekelaghel@gmail.com

Project Link: [\[https://github.com/yourusername/pdf-document-processor\](https://github.com/yourusername/pdf-document-processor)](https://github.com/it-malek/quick_projects/tree/main/pdf-document-processor)

