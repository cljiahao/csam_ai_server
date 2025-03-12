import cv2
import numpy as np

from apis.v2.helpers.processor.batch_processor import BatchProcessor
from apis.v2.helpers.processor.chip_processor import ChipProcessor
from constants.colors import BGRColors
from constants.image_thresholds import ImageThreshold
from db.models.image_settings import ImageSettings
from schemas.contours import ContourInfo, ContourList
from utils.image_process.blob_handler import BlobHandler
from utils.image_process.border_creator import BorderCreator
from utils.image_process.contour_handler import ContourHandler
from utils.image_process.mask_handler import MaskHandler


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
        contours, ImageThreshold.DENOISE_THRESHOLD
    )


def process_batch(mask_handler: MaskHandler, image_settings: ImageSettings):
    """Processes the image in batches."""
    batch_processor = BatchProcessor(
        mask_handler, image_settings.batch_erode, image_settings.batch_close
    )
    batch_processor.get_batch_data()
    return batch_processor


def process_chip(
    mask_handler: MaskHandler, border_pad: int, image_settings: ImageSettings
):
    """Processes the chip data from the mask handler."""
    chip_processor = ChipProcessor(
        mask_handler,
        image_settings.chip_erode,
        image_settings.chip_close,
        border_pad,
        image_settings.crop_size,
    )
    return chip_processor


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
