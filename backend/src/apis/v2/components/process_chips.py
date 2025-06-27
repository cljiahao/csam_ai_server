import cv2
import math
import numpy as np
from PIL import Image

from apis.v2.components.utils_image_process import create_contour_list
from apis.v2.schemas.common import ChipThreshold
from constants.colors import BGRColors
from db.models.image_settings import ImageSettings
from schemas.contours import ContourInfo, ContourInfoList
from utils.debug import timer
from utils.image_process.blob_handler import BlobHandler
from utils.image_process.contour_handler import ContourHandler


@timer("Find Combined Chip Contours (Black and Non Black)")
def create_chip_contour_info_list(
    border_image: np.ndarray, binary_image: np.ndarray, image_settings: ImageSettings
) -> tuple[ContourInfoList, ContourInfoList]:
    black_contour_info_list = find_black_contours(border_image)
    non_black_contour_info_list = find_non_black_contours(binary_image, image_settings)

    chip_threshold = update_chip_threshold(non_black_contour_info_list)
    crop_size = image_settings.crop_size

    black_refined_contour_infos = extract_refined_contour_info_list(
        black_contour_info_list, border_image, crop_size, chip_threshold
    )
    non_black_refined_contour_infos = extract_refined_contour_info_list(
        non_black_contour_info_list, border_image, crop_size, chip_threshold
    )

    return black_refined_contour_infos, non_black_refined_contour_infos, chip_threshold


def find_black_contours(image: np.ndarray) -> ContourInfoList:
    """Finds contours of black regions in the image."""
    black_mask_chip = create_black_chip_mask(image)
    return create_contour_list(black_mask_chip)


def create_black_chip_mask(image: np.ndarray) -> np.ndarray:
    """Creates a binary mask for black chips in the image."""
    ng_black = np.array(BGRColors.BLACK.value)
    black_mask = cv2.inRange(image, ng_black, ng_black)
    # TODO: Consider making the kernel size a constant
    open_kernel = BlobHandler.create_kernel(7)
    return cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, open_kernel)


def find_non_black_contours(
    binary_image: np.ndarray, image_settings: ImageSettings
) -> ContourInfoList:
    """Finds contours of non-black regions in the image."""
    non_black_mask_chip = apply_morphology_for_chips(
        binary_image,
        image_settings.chip_noise_erode,
        image_settings.chip_dilate,
        image_settings.chip_erode,
    )
    return create_contour_list(non_black_mask_chip)


def apply_morphology_for_chips(
    mask_image: np.ndarray, chip_noise_erode: int, chip_dilate: int, chip_erode: int
) -> np.ndarray:
    """Applies morphological operations to the binary mask."""
    noise_erode_kernel = BlobHandler.create_kernel(chip_noise_erode)
    noised_removed = cv2.erode(mask_image, noise_erode_kernel)

    dilate_kernel = BlobHandler.create_kernel(chip_dilate)
    dilated_image = cv2.dilate(noised_removed, dilate_kernel)

    erode_kernel = BlobHandler.create_kernel(chip_erode)
    eroded_image = cv2.erode(dilated_image, erode_kernel)

    return eroded_image


def update_chip_threshold(contour_infos: ContourInfoList) -> ChipThreshold:
    """Updates and returns chip threshold values based on the median contour area."""
    chip_threshold = ChipThreshold()
    median_area = contour_infos.get_median_area()
    chip_threshold.apply_ratios(median_area)
    return chip_threshold


def deform_chip_condition(threshold: ChipThreshold, contour: ContourInfo) -> bool:
    """Condition function to check if chip is deformed."""
    return threshold.LOWER_DEFECT_AREA <= contour.area <= threshold.UPPER_DEFECT_AREA


def check_single(
    contour: ContourInfo, image: np.ndarray, crop_size: int, threshold: int = 0
) -> ContourInfoList:
    """Analyzes a single contour, attempting to split it if its area exceeds a threshold."""
    if contour.area > threshold:
        drawn_roi = BlobHandler.draw_blob_mask_from_contours(image, contour.contour)
        ((x_center, y_center), _, _) = contour.rect
        crop_image = BlobHandler.crop_roi(drawn_roi, x_center, y_center, crop_size // 2)

        new_contours = BlobHandler.split_blobs_with_erosion(crop_image, drawn_roi)
        if new_contours:
            clean_contours = ContourHandler.filter_and_build_contour_info(new_contours)
            return ContourHandler.rotate_contour_upright(clean_contours)

    return ContourInfoList(contours=[contour])


def extract_refined_contour_info_list(
    contour_infos: ContourInfoList,
    image: np.ndarray,
    crop_size: int,
    threshold: ChipThreshold,
) -> list[ContourInfo]:
    """Extracts and refines a list of contours by splitting large ones and filtering by area."""
    return [
        split_contour_info
        for contour_info in contour_infos
        for split_contour_info in check_single(
            contour_info, image, crop_size, threshold.UPPER_CHIP_AREA
        ).contours
        if chip_out_of_spec(threshold, split_contour_info)
    ]


def chip_out_of_spec(threshold: ChipThreshold, contour: ContourInfo) -> bool:
    """Condition to check if contour is within threshold set for chips."""
    return threshold.LOWER_CHIP_AREA < contour.area < threshold.UPPER_CHIP_AREA


def rotate_and_crop_chip_image(
    contour_info: ContourInfo, border_image: np.ndarray, padding: int, crop_size: int
) -> np.ndarray:
    """Rotates and crops a chip image based on its contour information."""
    (x_center, y_center), _, theta = contour_info.rect

    pre_crop_image = BlobHandler.crop_roi(border_image, x_center, y_center, padding)
    pil_image = Image.fromarray(pre_crop_image)
    rotated_image = np.asarray(pil_image.rotate(theta))

    return BlobHandler.crop_roi(rotated_image, padding, padding, crop_size // 2)
