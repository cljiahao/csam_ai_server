import cv2
import numpy as np

from constants.colors import BGRColors
from constants.image_thresholds import ImageThreshold
from schemas.contours import ContourInfo, ContourList
from utils.image_process.blob_handler import BlobHandler
from utils.image_process.border_creator import BorderCreator
from utils.image_process.contour_handler import ContourHandler


def create_border(image: np.ndarray, padding: int = 0, crop_size: int = 0):
    """Creates border images and returns border image data."""
    border_creator = BorderCreator(image, padding, crop_size)
    border_gray = border_creator.convert_background_white_and_grayscale()
    border_blank = border_creator.create_blank_image()
    border_pad = border_creator.border_pad

    return border_creator.border_image, border_gray, border_blank, border_pad


def create_contour_list(mask_image: np.ndarray) -> ContourList:
    contours, _ = cv2.findContours(
        mask_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    return ContourHandler.filter_and_build_contour_info(
        contours, ImageThreshold.DENOISE_THRESHOLD.value
    )


def check_single(
    contour_info: ContourInfo,
    blank: np.ndarray,
    crop_size: int,
    check_single_threshold: int = 0,
) -> ContourList:
    """Analyzes a single contour and attempts to split it using erosion."""

    if contour_info.area > check_single_threshold:
        drawn_roi = cv2.drawContours(
            blank.copy(), contour_info.contour, -1, BGRColors.WHITE, -1
        )
        ((x_center, y_center), _, _) = contour_info.rect
        crop_image = BlobHandler.crop_roi(drawn_roi, x_center, y_center, crop_size // 2)

        new_contours = BlobHandler.erode_and_find_contours(crop_image)
        if new_contours:
            return ContourHandler.filter_and_build_contour_info(new_contours)

    return ContourList(contours=[contour_info])
