import os
import cv2
from concurrent.futures import ThreadPoolExecutor


def thread_write_images(batches: dict, ng_dict: dict, temp_path: str, ai: bool = False):
    """Write image to folder in a thread and return chip data"""
    # Format data for frontend and write images
    chip_dict = {}
    for i in range(batches):
        chip_dict[f"{i+1}"] = []

    with ThreadPoolExecutor() as exe:
        _ = [
            exe.submit(write_image, chip_dict, temp_path, key, value, ai)
            for key, value in ng_dict.items()
        ]

    return chip_dict


def write_image(
    chip_dict: dict,
    temp_path: str,
    file_name: str,
    img: cv2.typing.MatLike,
    ai: bool,
):
    """Write image to folder"""

    if ai:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(os.path.join(temp_path, file_name), img)

    update_chip_dict(chip_dict, file_name)


def update_chip_dict(chip_dict: dict, file_name: str) -> None:
    """Update dictionary with batch as key and value of a list of file_names"""

    batch = file_name.split("_")[1]

    if batch == "0":
        batch = "Stray"
    if batch not in chip_dict:
        chip_dict[batch] = []
    chip_dict[batch].append(file_name)
