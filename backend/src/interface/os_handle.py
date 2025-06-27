from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np


class FileManagerInterface(ABC):
    """Abstract interface for file management."""

    @abstractmethod
    def archive_existing_file(self, file_path: Path) -> None:
        """Archive existing files with the same name."""
        pass


class ImageManagerInterface(FileManagerInterface):
    """Abstract interface for image file management."""

    @abstractmethod
    def save_image(self, file_path: Path, image: np.ndarray) -> None:
        pass
