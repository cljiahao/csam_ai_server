import cv2
import numpy as np

from core.logging import logger


def get_batch(gray: cv2.typing.MatLike, batch_set: dict):
    """Main function to call sub functions for retrieving batch data"""

    mask_img = mask_batch(gray, batch_set["erode"], batch_set["close"])
    batch_data = find_batch(mask_img)

    return batch_data


def mask_batch(gray: cv2.typing.MatLike, erode: tuple, close: tuple):
    """Return masked image after threshold and morphological transformations"""

    _, ret = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    # Erode to prevent merging between batches
    erode = cv2.morphologyEx(ret, cv2.MORPH_ERODE, np.ones(erode, np.uint8))
    # Close to merge neighbouring chips to form a huge blob mask
    morph = cv2.morphologyEx(erode, cv2.MORPH_CLOSE, np.ones(close, np.uint8))

    return morph


def find_batch(mask_img: cv2.typing.MatLike):
    """Return a list of batch coordinates"""

    # Use to remove noises (Stray Chips / Dirt)
    img_height, img_width = mask_img.shape[:2]
    thres_area = img_height * img_width * 0.01

    batch_data = []

    contours, _ = cv2.findContours(mask_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        (_, (width, height), _) = cv2.minAreaRect(cnt)
        blob_area = width * height

        if thres_area < blob_area:
            x, y, w, h = cv2.boundingRect(cnt)
            xc, yc = x + w / 2, y + h / 2

            # Factor depends on the size of image (RoundUp)
            factor = -(-img_height // 1000) * 1000
            index = round(yc / factor, 1) * factor**2 + xc
            data = {"index": index, "x1": x, "y1": y, "x2": x + w, "y2": y + h}
            batch_data.append(data)

    batch_data = sorted(batch_data, key=lambda x: x["index"])
    logger.debug("Number of Batches found: %s", len(batch_data))

    return batch_data


def find_batch_no(x: float, y: float, batch_data: list):
    """Return batch number from coordinates compared to batch list"""

    batch_no = 0
    for i, coor in enumerate(batch_data):
        if x <= coor["x2"] and x >= coor["x1"] and y <= coor["y2"] and y >= coor["y1"]:
            batch_no = i + 1
            break

    return batch_no
