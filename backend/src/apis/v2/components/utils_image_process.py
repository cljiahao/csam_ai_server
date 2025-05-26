import cv2
import math
import numpy as np

from apis.v2.constants.csam_thresholds import CSAMThresholdRatio
from constants.colors import BGRColors
from schemas.contours import ContourInfo, ContourInfoList
from utils.image_process.blob_handler import BlobHandler
from utils.image_process.border_creator import BorderCreator
from utils.image_process.contour_handler import ContourHandler


def create_contour_list(
    mask_image: np.ndarray,
    denoise_threshold: int = CSAMThresholdRatio.DENOISE_THRESHOLD,
) -> ContourInfoList:
    """Finds contours in a binary image and creates a list of ContourInfo."""
    contours, _ = cv2.findContours(
        mask_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    return ContourHandler.filter_and_build_contour_info(contours, denoise_threshold)


def convert_white_bg_to_gray_to_binary(image: np.ndarray) -> np.ndarray:
    """Converts BGR image to white background, to grayscale and binary mask"""
    border_gray = BorderCreator.convert_background_white_and_grayscale(
        image, CSAMThresholdRatio.BACKGROUND_THRESHOLD
    )
    bright_bg_threshold = CSAMThresholdRatio.BRIGHT_BACKGROUND_THRESHOLD
    _, binary_image = cv2.threshold(
        border_gray, bright_bg_threshold, 255, cv2.THRESH_BINARY_INV
    )
    return binary_image


def focus_blob_body_mask(
    mask_image: np.ndarray, contour_info: ContourInfo
) -> np.ndarray:
    """Creates a mask focusing on the main body of a blob."""
    width, height = contour_info.rect[1]
    shortest = width if width < height else height
    minor_border = int((mask_image.shape[0] - shortest * 0.8) // 2)
    return BorderCreator.change_border_color(mask_image, minor_border, 0)


def get_base_image_mask(base_image: np.ndarray) -> np.ndarray:
    """Gets the mask of the base image."""
    base_roi_image = focus_center_blob(base_image)
    base_mask, _ = get_largest_blob_mask_and_info(base_roi_image)
    return base_mask


def get_defect_image_mask(ng_image: np.ndarray) -> np.ndarray:
    """Gets the defect mask of an NG image."""
    ng_roi_image = focus_center_blob(ng_image)
    ng_mask_image, _ = get_largest_blob_mask_and_info(ng_roi_image)
    single_blob_ng_image = cv2.bitwise_and(ng_image, ng_image, mask=ng_mask_image)
    defect_mask, _ = get_non_red_black_mask_and_area_hsv(single_blob_ng_image)
    return defect_mask


def focus_center_blob(image: np.ndarray) -> np.ndarray:
    """Focuses on the central blob of an 3D image by changing the border color."""
    major_border = math.floor(image.shape[0] / 4 * 0.7)
    return BorderCreator.change_border_color(
        image, major_border, BGRColors.BACKGROUND.value
    )


def get_largest_blob_mask_and_info(image: np.ndarray) -> tuple[np.ndarray, ContourInfo]:
    """Extracts the mask and contour information of the largest blob in an image."""
    bg_threshold = CSAMThresholdRatio.BACKGROUND_THRESHOLD
    white_bg_image = BorderCreator.convert_background_white(image, bg_threshold)
    white_bg_threshold = CSAMThresholdRatio.BRIGHT_BACKGROUND_THRESHOLD
    erode_mask = BlobHandler.extract_dark_blobs_mask(white_bg_image, white_bg_threshold)

    contour_info_list = create_contour_list(erode_mask)
    largest_contour_info = max(contour_info_list.contours, key=lambda x: x.area)
    largest_blob_mask = BlobHandler.draw_blob_mask_from_contours(
        image, largest_contour_info.contour
    )

    return largest_blob_mask, largest_contour_info


def get_non_red_black_mask_and_area_hsv(image: np.ndarray) -> tuple[np.ndarray, int]:
    """Calculates the area of pixels within a specified HSV range."""
    hsv_mask = BlobHandler.get_non_red_and_black_mask(image)
    hsv_area_sum = np.count_nonzero(hsv_mask)
    return hsv_mask, hsv_area_sum
