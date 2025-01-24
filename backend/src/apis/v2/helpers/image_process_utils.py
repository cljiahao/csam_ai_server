import cv2
import numpy as np

from apis.v2.helpers.processor.defect_processor import DefectProcessor
from constants.colors import BGRColors
from schemas.chips_data import DefectBatch, ImageData
from schemas.contours import ContourInfo, ContourList
from utils.image_process.blob_handler import BlobHandler
from utils.image_process.contour_handler import ContourHandler


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


def filter_contours(
    defect_processor: DefectProcessor,
    base_file_name: str,
    image: np.ndarray,
    border_pad: int,
    chunked_contours: list[list[ContourInfo]],
) -> tuple[dict[str, DefectBatch], list[ImageData], list[ImageData]]:
    """Processes and classifies contours into defect batches."""

    common_chunk_len = len(chunked_contours[0])
    for i, contour_chunk in enumerate(chunked_contours):
        start_index = i * common_chunk_len
        process_chunk(
            defect_processor,
            base_file_name,
            start_index,
            image,
            border_pad,
            contour_chunk,
        )

    return (
        defect_processor.defect_batch_dict,
        defect_processor.to_predict_list,
        defect_processor.defect_list,
    )


def process_chunk(
    defect_processor: DefectProcessor,
    base_file_name: str,
    start_index: int,
    image: np.ndarray,
    border_pad: int,
    contour_chunk: list[ContourInfo],
):
    """Processes a chunk of contours to classify chips and update defect batches."""
    for j, contour_info in enumerate(contour_chunk):
        if (
            defect_processor.chip_threshold.lower_chip_area
            < contour_info.area
            < defect_processor.chip_threshold.upper_chip_area
        ):

            chip_count = start_index + j
            file_name = f"{base_file_name}_{chip_count}.png"

            defect_processor.process_defects(
                file_name,
                image,
                border_pad,
                contour_info,
            )
