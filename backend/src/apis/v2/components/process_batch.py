import cv2
import numpy as np

from apis.v2.components.utils_image_process import create_contour_list
from core.logging import logger
from db.models.image_settings import ImageSettings
from schemas.contours import ContourInfoList
from utils.debug import timer
from utils.image_process.blob_handler import BlobHandler


@timer("Find Batch Contours")
def create_batch_contour_info_list(
    binary_image: np.ndarray, image_settings: ImageSettings
) -> ContourInfoList:
    batch_mask = apply_morphology_for_batch(
        binary_image, image_settings.batch_erode, image_settings.batch_close
    )
    return create_contour_list(batch_mask)


def apply_morphology_for_batch(
    mask_image: np.ndarray, batch_erode: int, batch_close: int
) -> np.ndarray:
    """Applies morphological operations to the binary mask."""
    erode_kernel = BlobHandler.create_kernel(batch_erode)
    eroded_image = cv2.erode(mask_image, erode_kernel)

    close_kernel = BlobHandler.create_kernel(batch_close)
    closed_image = cv2.morphologyEx(eroded_image, cv2.MORPH_CLOSE, close_kernel)

    return closed_image


def get_batch_data_from_contour_info(
    image: np.ndarray,
    contour_info_list: ContourInfoList,
) -> list[dict[str, float]]:
    """Generates batch data from contour information."""
    batch_data = []
    image_height, image_width = image.shape[:2]
    threshold_area = image_height * image_width * 0.01
    factor = image_height - image_height % -1000

    for contour_info in contour_info_list.contours:
        if contour_info.area < threshold_area:
            continue
        x, y, w, h = cv2.boundingRect(contour_info.contour)
        xc, yc = x + w / 2, y + h / 2
        index = round(yc / factor, 1) * factor**2 + xc

        batch_data.append({"index": index, "x1": x, "y1": y, "x2": x + w, "y2": y + h})

    batch_data = sorted(batch_data, key=lambda x: x["index"])
    logger.debug("Number of Batches found: %s", len(batch_data))

    return batch_data


def find_batch_no(
    batch_data: list[dict[str, float]], coordinates: list[int, int]
) -> str:
    """Finds the batch number for the given coordinates."""
    x, y = coordinates
    for i, coord in enumerate(batch_data):
        if coord["x1"] <= x <= coord["x2"] and coord["y1"] <= y <= coord["y2"]:
            return str(i + 1)
    return "Stray"
