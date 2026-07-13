import os
import shutil
from typing import List

class DirectoryManager:
    @staticmethod
    def create_directories(root_path: str, directories: List[str]) -> None:
        for directory in directories:
            path = os.path.join(root_path, directory)
            os.makedirs(path, exist_ok=True)

    @staticmethod
    def cleanup(root_path: str) -> None:
        if os.path.exists(root_path):
            shutil.rmtree(root_path, ignore_errors=True)

    @staticmethod
    def verify_structure(root_path: str, directories: List[str]) -> bool:
        for directory in directories:
            path = os.path.join(root_path, directory)
            if not os.path.isdir(path):
                return False
        return True
