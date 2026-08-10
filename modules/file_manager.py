import os
from pathlib import Path

class LocalFileManager:
    """
    Autonomous local file operations engine.
    Allows the AI assistant to read, write, update, and search files on the user's computer.
    """

    @staticmethod
    def write_file(file_path: str, content: str) -> str:
        """Creates or overwrites a file with the given content."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return f"Successfully wrote file to: {path.resolve()}"

    @staticmethod
    def read_file(file_path: str) -> str:
        """Reads the content of a local file."""
        path = Path(file_path)
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        return path.read_text(encoding='utf-8', errors='ignore')

    @staticmethod
    def list_files(directory_path: str = ".") -> list:
        """Lists all files in a directory."""
        path = Path(directory_path)
        if not path.exists():
            return [f"Directory '{directory_path}' does not exist."]
        return [str(p) for p in path.glob("*")]
