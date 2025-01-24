import numpy as np
from fastapi import UploadFile
from concurrent.futures import ThreadPoolExecutor

from core.directory import directory
from schemas.chips_data import ImageData
from utils.debug import timer
from utils.os_handle.image_manager import ImageManager


@timer("Saving uploaded image")
def save_original_image(file: UploadFile, base_partial_path: str) -> np.ndarray:
    """Handles the uploaded image by saving it to the specified path after converting it to a NumPy array."""
    original_path = directory.images_dir / base_partial_path / "original"  # constant
    directory.create_folders([original_path])
    ImageManager.archive_existing_file(original_path, file.filename)
    image = ImageManager.file_to_image(file)
    ImageManager.save_image(original_path / file.filename, image)

    return image


@timer("Writing dissected images")
def thread_write_temp_images(base_partial_path: str, defect_list: list[ImageData]):
    """Saves a list of defect images to disk using concurrent threads."""
    temp_path = directory.images_dir / base_partial_path / "temp"  # constant
    directory.create_folders([temp_path])
    with ThreadPoolExecutor() as exe:
        _ = [
            exe.submit(
                ImageManager.save_image,
                str(temp_path / defect.file_name),
                defect.rotated_image,
            )
            for defect in defect_list
        ]
