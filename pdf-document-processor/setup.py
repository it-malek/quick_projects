from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pdf-document-processor",
    version="0.1.0",
    description="A utility for merging and organizing PDF documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Malek Elaghel",
    author_email="malekelaghel@gmail.com",
    url="https://github.com/it-malek/quick_projects/tree/main/pdf-document-processor",
    packages=find_packages(include=['src', 'src.*']),
    install_requires=[
        'pypdf>=3.0.0',
    ],
    python_requires=">=3.7",
)