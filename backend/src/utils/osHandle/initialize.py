import cv2
import numpy as np
from typing import IO
from pathlib import Path

from core.exceptions import ImageProcessError
from core.logging import logger


def initialize(
    lot_no: str, item: str, file: IO, base_path: Path
) -> tuple[np.ndarray, Path, Path]:
    """Initial checks and file saving."""

    plate_no = Path(file.filename).stem
    logger.debug("Plate No: %s", plate_no)

    plate_path = base_path / item / lot_no / plate_no

    # Create temp folder to store images temporary
    temp_path = plate_path / "temp"
    temp_path.mkdir(parents=True, exist_ok=True)

    image = save_original(file, plate_path)

    return image, plate_path, temp_path


def save_original(file: IO, plate_path: Path) -> np.ndarray:
    """Save original file and return MatLike image."""

    original_path = plate_path / "original"
    original_path.mkdir(parents=True, exist_ok=True)

    file_name = Path(file.filename)
    files_in_dir = list(original_path.glob("*"))
    if files_in_dir:
        # Rename file with same filename to archive it
        archive_name = file_name.stem + f"_{len(files_in_dir)}" + file_name.suffix
        archived_file = original_path / archive_name
        file_path = original_path / file_name
        if file_path.exists():
            file_path.rename(archived_file)

    try:
        # Convert file to numpy and decode into cv2
        file_content = file.file.read()
        np_image = np.frombuffer(file_content, dtype=np.uint8)
        image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        cv2.imwrite(str(original_path / file_name), image)
    except Exception as e:
        std_out = "Error converting file to cv2 format"
        logger.error(std_out, exc_info=True)
        raise ImageProcessError(std_out) from e

    return image
