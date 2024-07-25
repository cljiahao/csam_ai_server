import os
import cv2
import numpy as np
from typing import IO
from shutil import rmtree

from core.exceptions import ImageProcessError
from core.logging import logger


def initialize(
    lot_no: str, item: str, file: IO, base_path: str
) -> tuple[cv2.typing.MatLike, str, str]:
    """Initial checks and file saving"""

    plate_no = os.path.splitext(file.filename)[0]
    logger.debug("Plate No: %s", plate_no)

    plate_path = os.path.join(base_path, item, lot_no, plate_no)
    temp_path = check_temp_dir(lot_no, plate_path)

    image = save_original(file, plate_path)

    return image, plate_path, temp_path


def check_temp_dir(lot_no: str, plate_path: str) -> str:
    """Remove plate path and remake folder if testing"""

    if os.path.isdir(plate_path) and lot_no.lower()[:4] == "test":
        rmtree(plate_path)
    temp_path = os.path.join(plate_path, "temp")
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    return temp_path


def save_original(file: IO, plate_path: str):
    """Save original file and return MatLike image"""

    ori_path = os.path.join(plate_path, "original")
    if not os.path.exists(ori_path):
        os.makedirs(ori_path)

    file_name = file.filename
    no_of_files = len(os.listdir(ori_path))
    if no_of_files > 0:
        # Rename file with same filename to archive it
        f_name, ext = os.path.splitext(file.filename)
        archive_name = f"{f_name}_{no_of_files}{ext}"
        os.rename(
            os.path.join(ori_path, file_name), os.path.join(ori_path, archive_name)
        )

    try:
        # Convert file to numpy and decode into cv2
        np_img = np.asarray(bytearray(file.file.read()))
        image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        cv2.imwrite(os.path.join(ori_path, file_name), image)
    except Exception as e:
        std_out = "Error converting file to cv2 format"
        logger.error(std_out, exc_info=True)
        raise ImageProcessError(std_out)

    return image
