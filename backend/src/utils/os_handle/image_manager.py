import cv2
from fastapi import UploadFile
from pathlib import Path
import numpy as np

from core.logging import logger
from core.exceptions import ImageProcessError
from interface.os_handle import ImageManagerInterface
from utils.debug import error_handler


class ImageManager(ImageManagerInterface):
    @staticmethod
    def archive_existing_file(folder_path: Path, file_name: str) -> None:
        """Archives an existing file in the specified folder by renaming it with an index."""
        files_in_dir = list(folder_path.glob("*"))
        file_path = folder_path / file_name
        if files_in_dir and file_path.exists():
            # Rename file with same filename to archive it
            archive_name = file_path.stem + f"_{len(files_in_dir)}" + file_path.suffix
            archived_file_path = folder_path / archive_name
            file_path.rename(archived_file_path)
            logger.info(f"Archived file: {file_path} to {archived_file_path}")

    @staticmethod
    @error_handler(
        print_message="Error converting file to cv2 format",
        custom_error=ImageProcessError,
    )
    def file_to_image(file: UploadFile) -> np.ndarray:
        """Converts an uploaded file to an OpenCV image."""
        file_content = file.file.read()
        np_image = np.frombuffer(file_content, dtype=np.uint8)
        image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        if image is None:
            raise Exception()
        return image

    @staticmethod
    @error_handler(
        print_message="Error saving image to disk",
        custom_error=ImageProcessError,
    )
    def save_image(file_path: str | Path, image: np.ndarray) -> None:
        """Saves a NumPy array as an image file."""
        if isinstance(file_path, Path):
            file_path = str(file_path)
        cv2.imwrite(file_path, image)
