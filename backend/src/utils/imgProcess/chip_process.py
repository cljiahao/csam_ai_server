import os
import cv2
import math
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

from core.config import settings
from core.exceptions import ImageProcessError
from core.logging import logger
from utils.imgProcess.batch_process import find_batch_no


def get_chips(
    b_img: cv2.typing.MatLike,
    b_gray: cv2.typing.MatLike,
    batch_data: list,
    chip_set: dict,
    ai: bool = False,
) -> tuple[int, dict, dict]:
    """Main function to call sub functions for retrieiving chip data"""

    mask = mask_chips(b_gray, chip_set["erode"], chip_set["close"])
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    clean_contours = [x for x in contours if cv2.contourArea(x) > 50]
    if len(clean_contours) == 0:
        std_out = "Contour length = 0, unable to find median area."
        logger.error(std_out)
        raise ImageProcessError(std_out)

    avg_chip_area = get_median_area(clean_contours)

    # Update Threshold range with median area of chips
    thres_range = {}
    for k, v in settings.THRES_RANGE.items():
        thres_range[k] = v * avg_chip_area

    chunk_contours = chunking(clean_contours)

    no_of_chips = 0
    temp_dict, ng_dict = {}, {}
    pad = [math.ceil(x * math.sqrt(2) / 10) * 10 for x in settings.CHIP_IMG_SIZE]
    try:
        with ThreadPoolExecutor() as exe:
            for cnts in chunk_contours:
                no_of_chips = exe.submit(
                    find_chips,
                    b_img,
                    batch_data,
                    cnts,
                    no_of_chips,
                    temp_dict,
                    ng_dict,
                    thres_range,
                    pad,
                    ai,
                ).result()
    except Exception as e:
        std_out = "Error dissecting chips individually"
        logger.error(std_out, exc_info=True)
        raise ImageProcessError(std_out) from e

    logger.debug("Number of Chips  %s", no_of_chips)

    return no_of_chips, temp_dict, ng_dict


def mask_chips(
    gray: cv2.typing.MatLike, erode_val: tuple, close_val: tuple
) -> cv2.typing.MatLike:
    """Return masked image after threshold and morphological transformations"""

    _, ret = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    # Erode to remove noises surrounding chips
    erode = cv2.morphologyEx(ret, cv2.MORPH_ERODE, np.ones(erode_val, np.uint8))
    # Close to fill up holes in chips
    close = cv2.morphologyEx(erode, cv2.MORPH_CLOSE, np.ones(close_val, np.uint8))

    return close


def chunking(contours: list[cv2.typing.MatLike]) -> list[list[cv2.typing.MatLike]]:
    """Chunk contours list to sizeable chunks based on cpu core for multiprocessing"""

    cpu_cnt = os.cpu_count()
    chunk_size = int(len(contours) / cpu_cnt)
    chunk_contours = [
        contours[i : i + chunk_size] for i in range(0, len(contours), chunk_size)
    ]
    logger.debug("Chunk size : %s based on CPU Count : %s", chunk_size, cpu_cnt)

    return chunk_contours


def get_median_area(contours: list[cv2.typing.MatLike]) -> float:
    """Get median area of all chips found in mask"""

    contour_areas = [cv2.contourArea(x) for x in contours]
    # Average contour area of the chips
    avg_chip_area = np.median(contour_areas)
    logger.debug("Average Chip Area is %s", avg_chip_area)

    return avg_chip_area


def find_chips(
    b_img: cv2.typing.MatLike,
    batch_data: list,
    cnts: list[cv2.typing.MatLike],
    chip_no: int,
    temp_dict: dict,
    ng_dict: dict,
    thres_range: dict,
    pad: list[int],
    ai: bool,
):
    for cnt in cnts:

        cnt_arr = check_single(
            thres_range["upp_def_area"], cv2.contourArea(cnt), b_img, cnt
        )

        for c in cnt_arr:
            chip_area = cv2.contourArea(c)
            if thres_range["low_chip_area"] < chip_area < thres_range["upp_chip_area"]:

                rect = cv2.minAreaRect(c)
                ((xc, yc), _, _) = rect
                batch = find_batch_no(xc, yc, batch_data)
                chip_no += 1
                # 0 first element of name is to indicate image not selected yet
                # xc, yc - pad to remove the the added borders previously
                fName = "{}_{}_{}_{}_{}.png".format(
                    0,
                    batch,
                    chip_no,
                    int(xc - pad[0]),
                    int(yc - pad[1]),
                )

                rotated_img = rotate_chips(b_img, rect, pad)
                # Convert colour to RGB for AI Model to predict properly
                if ai:
                    rotated_img = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2RGB)

                # Reduce predict data to quicken processing time
                # Chips below certain threshold are considered defects
                if (
                    chip_area < thres_range["low_def_area"]
                    or thres_range["upp_def_area"] < chip_area
                ):
                    ng_dict[fName] = rotated_img
                else:
                    temp_dict[fName] = rotated_img

    return chip_no


def check_single(
    upp_chip_area: float,
    chip_area: float,
    img: cv2.typing.MatLike,
    cnt: cv2.typing.MatLike,
):
    """Return list of broken down contours"""
    if upp_chip_area < chip_area:
        blank = np.zeros(img.shape[:2], np.uint8)
        cv2.drawContours(blank, [cnt], -1, (255, 255, 255), -1)

        ((x, y), _, _) = cv2.minAreaRect(cnt)
        x_crop, y_crop = settings.CHIP_IMG_SIZE
        crop = blank[
            int(y - y_crop / 2) : int(y + y_crop / 2),
            int(x - x_crop / 2) : int(x + x_crop / 2),
        ]

        for i in range(3, 9):
            crop[:] = cv2.erode(crop, np.ones((i, i), np.uint8))
            new_cnts, _ = cv2.findContours(
                blank, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            if len(new_cnts) > 1:
                return new_cnts

    return [cnt]


def rotate_chips(img: cv2.typing.MatLike, rect: cv2.typing.RotatedRect, pad: list[int]):
    """Return rotated MatLike image cropped to specified size"""

    ((x, y), (width, height), theta) = rect
    if height < width:
        theta = theta - 90

    crop = img[
        int(y - pad[1]) : int(y + pad[1]),
        int(x - pad[0]) : int(x + pad[0]),
    ]

    im_pil = Image.fromarray(crop)
    rot_img = im_pil.rotate(theta)
    rot_img = np.asarray(rot_img)

    x_crop, y_crop = settings.CHIP_IMG_SIZE
    rot_img = rot_img[
        int(pad[1] - y_crop / 2) : int(pad[1] + y_crop / 2),
        int(pad[0] - x_crop / 2) : int(pad[0] + x_crop / 2),
    ]

    return rot_img
