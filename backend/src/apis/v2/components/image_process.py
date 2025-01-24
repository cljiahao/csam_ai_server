import cv2
import numpy as np

from apis.v2.helpers.image_process_utils import (
    check_single,
    filter_contours,
)
from apis.v2.helpers.processor.batch_processor import BatchProcessor
from apis.v2.helpers.processor.chip_processor import ChipProcessor
from apis.v2.helpers.processor.defect_processor import DefectProcessor
from constants.thresholds import ChipThreshold, ImageThreshold
from schemas.chips_data import DefectBatch
from schemas.contours import ContourList
from utils.debug import timer
from utils.image_process.border_creator import BorderCreator
from utils.image_process.contour_handler import ContourHandler
from utils.image_process.mask_handler import MaskHandler
from utils.services.train import (
    get_batch_settings,
    get_chip_settings,
    get_crop_settings,
)


@timer("Process CSAM Image")
def process_csam_image(
    image: np.ndarray, item: str, lot_no: str, plate_no: str
) -> tuple[dict[str, DefectBatch], list, list]:
    """Main function for processing the input image."""

    # Get crop size
    crop_size = get_crop_settings(item)

    # Border Creation
    border_image, border_gray, border_blank, border_pad = create_border(
        image, crop_size
    )

    # Mask Processing
    mask_handler = MaskHandler(border_gray)

    # Batch Processing
    batch_processor = process_batch(mask_handler, item)

    # Chip Processing
    chip_processor = process_chip(mask_handler, item, border_pad, crop_size)

    # Chip Threshold instantiate
    chip_threshold = ChipThreshold()

    refined_contours_info_list = split_and_refine_contours(
        chip_threshold,
        chip_processor.chip_mask,
        border_blank,
        crop_size,
    )

    # Defect Processing
    defect_processor = DefectProcessor(batch_processor, chip_processor, chip_threshold)

    defect_batch_dict, to_predict_list, defect_list = process_chunk_contours(
        defect_processor,
        lot_no,
        plate_no,
        refined_contours_info_list,
        border_image,
        border_pad,
    )

    return defect_batch_dict, to_predict_list, defect_list


@timer("Border creation")
def create_border(image: np.ndarray, crop_size: int):
    """Creates border images and returns relevant data."""
    border_creator = BorderCreator(image, crop_size)
    border_gray = border_creator.convert_background_white_and_grayscale()
    border_blank = border_creator.create_blank_image()
    border_pad = border_creator.border_pad

    return border_creator.border_image, border_gray, border_blank, border_pad


@timer("Batch processing")
def process_batch(mask_handler: MaskHandler, item: str):
    """Processes the image in batches."""
    batch_erode, batch_close = get_batch_settings(item)
    batch_processor = BatchProcessor(mask_handler, batch_erode, batch_close)
    batch_processor.get_batch_data()
    return batch_processor


@timer("Chip processing")
def process_chip(mask_handler: MaskHandler, item: str, border_pad: int, crop_size: int):
    """Processes the chip data from the mask handler."""
    chip_erode, chip_close = get_chip_settings(item)
    chip_processor = ChipProcessor(
        mask_handler, chip_erode, chip_close, border_pad, crop_size
    )
    return chip_processor


@timer("Split and refining")
def split_and_refine_contours(
    chip_threshold: ChipThreshold,
    mask_image: np.ndarray,
    blank: np.ndarray,
    crop_size: int,
) -> ContourList:
    """Split and refine contours using BlobHandler."""

    contours, _ = cv2.findContours(
        mask_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    contour_info_list = ContourHandler.filter_and_build_contour_info(
        contours, ImageThreshold.DENOISE_THRESHOLD
    )

    median_area = contour_info_list.get_median_area()
    chip_threshold.apply_ratios(median_area)

    refined_contours = [
        split_contour
        for contour_info in contour_info_list.contours
        for split_contour in check_single(
            contour_info, blank, crop_size, chip_threshold.upper_chip_area
        ).contours
    ]

    return ContourList(contours=refined_contours)


@timer("Chunk contour processing")
def process_chunk_contours(
    defect_processor: DefectProcessor,
    lot_no: str,
    plate_no: str,
    refined_contours_info_list: ContourList,
    image: np.ndarray,
    border_pad: int,
):
    """Processes contours in chunks, filtering and preparing defect data for further prediction."""
    base_file_name = f"{lot_no}_{plate_no}"
    chunked_contours = ContourHandler.chunking(refined_contours_info_list.contours)
    defect_batch_dict, to_predict_list, defect_list = filter_contours(
        defect_processor,
        base_file_name,
        image,
        border_pad,
        chunked_contours,
    )

    return defect_batch_dict, to_predict_list, defect_list
