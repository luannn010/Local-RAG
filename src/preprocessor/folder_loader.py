from src.preprocessor.file_processor import is_supported_file, load_file
import os

class FolderLoader:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.documents = {}

    def load(self) -> dict:
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                path = os.path.join(root, file)
                if is_supported_file(path):
                    try:
                        self.documents[path] = load_file(path)
                    except Exception as e:
                        print(f"Failed to process {path}: {e}")
        return self.documents