import os
import cv2
import math
import numpy as np

from core.exceptions import ImageProcessError
import core.constants as core_consts
import utils.imageProcess.constants as imageProcess_constants
from core.logging import logger


def create_border_image(image: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return border extended MatLike image in BGR and Gray."""

    # Added border to include chips near the edge of images,
    # allowing better cropping of chips later on
    padx, pady = [
        math.ceil(x * math.sqrt(2) / 10) * 10 for x in core_consts.CHIP_CROP_SIZE
    ]
    border_image = cv2.copyMakeBorder(
        image,
        pady,
        pady,
        padx,
        padx,
        cv2.BORDER_CONSTANT,
        value=imageProcess_constants.COLOR_BACKGROUND,
    )

    img = border_image.copy()
    # Convert background to white for easier thresholding
    background = np.all(img >= imageProcess_constants.BG_THRESHOLD, axis=-1)
    img[background] = imageProcess_constants.COLOR_WHITE
    border_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return border_image, border_gray


def denoise_mask_image(mask_image: np.ndarray) -> list[tuple[np.ndarray, float]]:
    """Mask the image and ignoring noises and return contours and area."""
    contours, _ = cv2.findContours(
        mask_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    clean_contours = []
    for cnt in contours:
        chip_area = cv2.contourArea(cnt)
        if chip_area > imageProcess_constants.DENOISE_THRESHOLD:
            clean_contours.append((cnt, chip_area))

    if not clean_contours:
        std_out = "Contour length = 0, unable to find median area."
        logger.error(std_out)
        raise ImageProcessError(std_out)

    return clean_contours


def chunking(contours: list[tuple[np.ndarray, float]]) -> list[list[np.ndarray]]:
    """Chunk contours list to sizeable chunks based on cpu core for multiprocessing."""

    cpu_count = os.cpu_count() or 1
    chunk_size = max(1, len(contours) // cpu_count)
    chunk_contours = [
        contours[i : i + chunk_size] for i in range(0, len(contours), chunk_size)
    ]
    logger.debug("Chunk size : %s based on CPU Count : %s", chunk_size, cpu_count)

    return chunk_contours


def get_median_area(contours: list[tuple[np.ndarray, float]]) -> float:
    """Calculate the median area of all chips found in the mask."""

    contour_areas = [area for (_, area) in contours]
    avg_chip_area = np.median(contour_areas)
    logger.debug("Average Chip Area is %s", avg_chip_area)

    return avg_chip_area


def find_batch_no(x: float, y: float, batch_data: list[dict[str, float]]) -> int:
    """Return batch number from coordinates compared to batch list."""

    for i, coor in enumerate(batch_data):
        if x <= coor["x2"] and x >= coor["x1"] and y <= coor["y2"] and y >= coor["y1"]:
            return i + 1

    return 0
