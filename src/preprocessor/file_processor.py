import os
import json
from typing import Union

def is_supported_file(file_path: str) -> bool:
    """Check if the file is a supported type."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    return ext in [".md", ".txt", ".pdf", ".json"]

def load_file(file_path: str) -> str:
    if not is_supported_file(file_path):
        raise ValueError(f"Unsupported file type: {file_path}")

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    match ext:
        case ".md" | ".txt":
            with open(file_path, "r") as f:
                return f.read()
        case ".pdf":
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        case ".json":
            with open(file_path, "r") as f:
                data = json.load(f)
                return json.dumps(data, indent=2)
        case _:
            raise ValueError(f"Unsupported file type: {ext}")