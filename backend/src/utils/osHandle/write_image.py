import cv2
import numpy as np
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def thread_write_images(
    batches: int, ng_dict: dict[str, np.ndarray], temp_path: Path, ai: bool = False
) -> dict[str, list[str]]:
    """Write image to folder in a thread and return chip data."""

    # Format data for frontend and write images
    chip_dict = {str(i + 1): [] for i in range(batches)}

    with ThreadPoolExecutor() as exe:
        futures = [
            exe.submit(write_image, chip_dict, temp_path, key, value, ai)
            for key, value in ng_dict.items()
        ]
        for future in futures:
            future.result()  # Ensure that all threads complete

    return chip_dict


def write_image(
    chip_dict: dict[str, list[str]],
    temp_path: Path,
    file_name: str,
    image: np.ndarray,
    ai: bool,
) -> None:
    """Write image to folder."""

    if ai:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(temp_path / file_name), image)

    update_chip_dict(chip_dict, file_name)


def update_chip_dict(chip_dict: dict[str, list[str]], file_name: str) -> None:
    """Update dictionary with batch as key and value of a list of file_names."""

    batch = file_name.split("_")[1]

    if batch == "0":
        batch = "Stray"
    if batch not in chip_dict:
        chip_dict[batch] = []
    chip_dict[batch].append(file_name)
