import numpy as np
from sqlalchemy.orm import Session

from apis.v2.helpers.image_process_utils import (
    check_single,
    create_border,
    create_contour_list,
)
from apis.v2.helpers.processor.batch_processor import BatchProcessor
from apis.v2.helpers.processor.chip_processor import ChipProcessor
from apis.v2.helpers.processor.defect_processor import DefectProcessor
from constants.chip_thresholds import ChipThreshold
from core.exceptions import MissingSettings
from db.models.image_settings import ImageSettings
from db.services.image_settings import ImageSettingsService
from schemas.chips_data import FileDataBatch
from schemas.contours import ContourList
from utils.debug import timer
from utils.image_process.mask_handler import MaskHandler
from services.train import get_image_settings


@timer("Pre Process Image")
def pre_process_image(
    image: np.ndarray, item: str, lot_no: str, plate_no: str, db: Session
) -> tuple[DefectProcessor, str, ContourList, np.ndarray, int]:
    """Main function for processing the input image."""

    # Fetch image settings (either from API or fallback to DB)
    image_settings = get_or_fetch_image_settings(item, db)

    # Border Creation
    border_image, border_gray, border_blank, border_pad = create_border(
        image, crop_size=image_settings.crop_size
    )

    # Mask Processing
    mask_handler = MaskHandler(border_gray)

    # Batch Processing
    batch_processor = process_batch(mask_handler, image_settings)

    # Chip Processing
    chip_processor = process_chip(mask_handler, border_pad, image_settings)

    # Chip Threshold instantiate
    chip_threshold = ChipThreshold()

    refined_contours_info_list = split_and_refine_contours(
        chip_threshold,
        chip_processor.chip_mask,
        border_blank,
        image_settings.crop_size,
    )

    # Defect Processing
    defect_processor = DefectProcessor(batch_processor, chip_processor, chip_threshold)

    base_file_name = f"{lot_no}_{plate_no}"

    return (
        defect_processor,
        base_file_name,
        refined_contours_info_list,
        border_image,
        border_pad
    )


@timer("Get Image Settings")
def get_or_fetch_image_settings(item: str, db: Session) -> ImageSettings:

    image_settings = get_image_settings(item)  # External API call

    image_settings_service = ImageSettingsService(db)

    if image_settings is not None:
        image_settings_service.create_or_update_image_settings(item, image_settings)
        return image_settings

    # Fall back to local database if API fails and returns None
    image_settings = image_settings_service.read_image_settings(item)
    if image_settings is None:
        raise MissingSettings(
            f"Image settings for '{item}' not found in API or database."
        )

    return image_settings


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


@timer("Split and refining")
def split_and_refine_contours(
    chip_threshold: ChipThreshold,
    chip_mask: np.ndarray,
    blank: np.ndarray,
    crop_size: int,
) -> ContourList:
    """Split and refine contours using BlobHandler."""

    contour_info_list = create_contour_list(chip_mask)

    median_area = contour_info_list.get_median_area()
    chip_threshold.apply_ratios(median_area)

    split_contours = [
        split_contour
        for contour_info in contour_info_list.contours
        for split_contour in check_single(
            contour_info, blank, crop_size, chip_threshold.UPPER_CHIP_AREA
        ).contours
    ]

    refined_contours = [
        contour
        for contour in split_contours
        if chip_threshold.LOWER_CHIP_AREA
        < contour.area
        < chip_threshold.UPPER_CHIP_AREA
    ]

    return ContourList(contours=refined_contours)
