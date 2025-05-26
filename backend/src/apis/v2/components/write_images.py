import numpy as np
from concurrent.futures import ThreadPoolExecutor

from apis.v2.schemas.csam_image import LabeledImageData
from constants.folder_names import CSAMImageFolderName
from core.directory_manager import directory_manager as dm
from utils.debug import timer
from utils.image_process.image_manager import ImageManager


@timer("Saving uploaded image")
def save_original_image(
    file_name: str, file_path: str, base_partial_path: str
) -> np.ndarray:
    """Handles the uploaded image by saving it to the specified path after converting it to a NumPy array."""
    original_path = dm.images_dir / base_partial_path / CSAMImageFolderName.ORIGINAL
    dm.create_directory(original_path)
    ImageManager.archive_existing_file(original_path, file_name)
    image = ImageManager.path_to_image(file_path)
    ImageManager.save_image(original_path / file_name, image)
    return image


@timer("Writing dissected images")
def thread_write_temp_images(
    base_partial_path: str, defect_list: list[LabeledImageData]
) -> None:
    """Saves a list of defect images to disk using concurrent threads."""
    temp_path = dm.images_dir / base_partial_path / CSAMImageFolderName.TEMP
    dm.create_directory(temp_path)
    with ThreadPoolExecutor() as exe:
        _ = [
            exe.submit(
                ImageManager.save_image,
                str(temp_path / defect.file_name),
                defect.image_data,
            )
            for defect in defect_list
        ]
