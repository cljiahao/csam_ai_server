import cv2
import math
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

import utils.imageProcess.constants as imageProcess_constants
from core.exceptions import ImageProcessError
from core.logging import logger
from utils.imageProcess.image_utils import (
    chunking,
    denoise_mask_image,
    find_batch_no,
    get_median_area,
)


def get_chips(
    border_image: np.ndarray,
    border_gray: np.ndarray,
    batch_data: list[dict[str, float]],
    chip_settings: dict,
    ai: bool = False,
) -> tuple[int, dict[str, np.ndarray], dict[str, np.ndarray]]:
    """Main function to call sub functions for retrieiving chip data."""

    mask_image = mask_chips(border_gray, chip_settings["erode"], chip_settings["close"])
    clean_contours = denoise_mask_image(mask_image)

    avg_chip_area = get_median_area(clean_contours)

    # Update Threshold range with median area of chips
    thres_range = {
        k: v * avg_chip_area for k, v in imageProcess_constants.THRESH_RANGE.items()
    }

    chunk_contours = chunking(clean_contours)

    no_of_chips = 0
    temp_dict, ng_dict = {}, {}
    crop_settings = chip_settings["crop"]
    pad = [math.ceil(x * math.sqrt(2) / 10) * 10 for x in chip_settings["crop"]]
    try:
        with ThreadPoolExecutor() as exe:
            for contours_metrics in chunk_contours:
                no_of_chips = exe.submit(
                    find_chips,
                    border_image,
                    batch_data,
                    contours_metrics,
                    no_of_chips,
                    temp_dict,
                    ng_dict,
                    thres_range,
                    pad,
                    ai,
                    crop_settings,
                ).result()
    except cv2.error as e:
        std_out = "OpenCV error occurred."
        logger.error(std_out, exc_info=True)
        raise ImageProcessError(std_out) from e
    except Exception as e:
        std_out = "Error dissecting chips individually."
        logger.error(std_out, exc_info=True)
        raise ImageProcessError(std_out) from e

    logger.debug("Number of Chips  %s", no_of_chips)

    return no_of_chips, temp_dict, ng_dict


def mask_chips(
    border_gray: np.ndarray, erode_val: tuple, close_val: tuple
) -> np.ndarray:
    """Return masked image after threshold and morphological transformations."""

    _, binary_image = cv2.threshold(border_gray, 250, 255, cv2.THRESH_BINARY_INV)

    # Apply morphological operations: erode and close
    kernel_erode = np.ones(erode_val, np.uint8)
    kernel_close = np.ones(close_val, np.uint8)

    # Erode to remove noises surrounding chips
    eroded_image = cv2.morphologyEx(binary_image, cv2.MORPH_ERODE, kernel_erode)
    # Close to fill up holes in chips
    closed_image = cv2.morphologyEx(eroded_image, cv2.MORPH_CLOSE, kernel_close)

    return closed_image


def find_chips(
    border_image: np.ndarray,
    batch_data: list[dict[str, float]],
    contours_metrics: list[tuple[np.ndarray, float]],
    chip_no: int,
    temp_dict: dict[str, np.ndarray],
    ng_dict: dict[str, np.ndarray],
    thres_range: dict[str, float],
    pad: list[int],
    ai: bool,
    crop_settings: list[str],
) -> int:
    """Find and process individual chips from the batch data."""

    for contour, chip_area in contours_metrics:
        contour_arr = check_single(
            border_image,
            contour,
            chip_area,
            thres_range["upp_chip_area"],
            crop_settings,
        )

        for cont, new_chip_area in contour_arr:
            if (
                thres_range["low_chip_area"]
                < new_chip_area
                < thres_range["upp_chip_area"]
            ):
                rect = cv2.minAreaRect(cont)
                ((xc, yc), _, _) = rect
                batch = find_batch_no(xc, yc, batch_data)
                chip_no += 1
                # 0 first element of name is to indicate image not selected yet
                # xc, yc - pad to remove the the added borders previously
                file_name = "{}_{}_{}_{}_{}.png".format(
                    0,
                    batch,
                    chip_no,
                    int(xc - pad[0]),
                    int(yc - pad[1]),
                )

                rotated_image = rotate_chips(border_image, rect, pad, crop_settings)
                # Convert colour to RGB for AI Model to predict properly
                if ai:
                    rotated_image = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)

                # Reduce predict data to quicken processing time
                # Chips below certain threshold are considered defects
                if (
                    new_chip_area < thres_range["low_def_area"]
                    or thres_range["upp_def_area"] < new_chip_area
                ):
                    ng_dict[file_name] = rotated_image
                else:
                    temp_dict[file_name] = rotated_image

    return chip_no


def check_single(
    border_image: np.ndarray,
    contour: np.ndarray,
    chip_area: float,
    upp_chip_area: float,
    crop_settings: list[str],
) -> list[np.ndarray]:
    """Return list of broken down contours."""

    if upp_chip_area < chip_area:
        blank = np.zeros(border_image.shape[:2], np.uint8)
        cv2.drawContours(blank, [contour], -1, (255, 255, 255), -1)

        x, y = np.intp(cv2.minAreaRect(contour)[0])
        x_crop, y_crop = crop_settings
        crop = blank[
            y - y_crop // 2 : y + y_crop // 2, x - x_crop // 2 : x + x_crop // 2
        ]

        # Erode image in a range or 3,3 to 9,9 to see if can break into more chips
        for i in range(3, 9):
            crop[:] = cv2.erode(crop, np.ones((i, i), np.uint8))
            new_cnts, _ = cv2.findContours(
                blank, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            if len(new_cnts) > 1:
                contour_arr = [(cnt, cv2.contourArea(cnt)) for cnt in new_cnts]
                return contour_arr

    return [(contour, chip_area)]


def rotate_chips(
    border_image: np.ndarray,
    rect: cv2.RotatedRect,
    pad: list[int],
    crop_settings: list[str],
) -> np.ndarray:
    """Return rotated image cropped to specified size."""

    ((x, y), (width, height), theta) = rect
    if height < width:
        theta -= 90

    crop = border_image[
        int(y - pad[1]) : int(y + pad[1]),
        int(x - pad[0]) : int(x + pad[0]),
    ]

    pil_image = Image.fromarray(crop)
    rotated_image = np.asarray(pil_image.rotate(theta))

    x_crop, y_crop = crop_settings
    rotated_image = rotated_image[
        pad[1] - y_crop // 2 : pad[1] + y_crop // 2,
        pad[0] - x_crop // 2 : pad[0] + x_crop // 2,
    ]

    return rotated_image
