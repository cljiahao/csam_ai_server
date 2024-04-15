import cv2
import numpy as np


def batch(b_gray, img_shape, batch_set) -> list:
    """Main function to call sub functions for retrieving batch data

    Parameters
    ----------
    gray : numpy array
        Gray Image for masking purposes
    img_shape : list
        Image Height and Width in a list
    item : str
        item associated with lot number

    Returns
    -------
    batch_data : list
        An array of each batches coordinate found in the form of
        [{index: int, x1: double, y1: double, x2: double, y2: double}...]
    """
    mask_img = mask_batch(b_gray, batch_set)
    batch_data = find_batch(mask_img, img_shape)

    return batch_data


def mask_batch(gray, batch_set):
    """
    Parameters
    ----------
    gray : numpy array
        Gray Image for masking purposes
    batch_set : dict
        Batch Settings information

    Returns
    -------
    morph : MatLike
        A masked image of non background
    """
    _, ret = cv2.threshold(gray, batch_set["threshold"], 255, cv2.THRESH_BINARY_INV)
    # Merge neighbouring chips to form a huge blob mask
    morph = cv2.morphologyEx(
        ret,
        cv2.MORPH_CLOSE,
        np.ones(
            (
                batch_set["close_y"],
                batch_set["close_x"],
            ),
            np.uint8,
        ),
    )
    # Erode to prevent merging between batches
    morph = cv2.morphologyEx(
        morph,
        cv2.MORPH_ERODE,
        np.ones(
            (
                batch_set["erode_y"],
                batch_set["erode_x"],
            ),
            np.uint8,
        ),
    )

    return morph


def find_batch(mask_img, img_shape) -> list:
    """
    Parameters
    ----------
    mask_img : MatLike
        A masked image of non background
    img_shape : list
        Image Height and Width in a list

    Returns
    -------
    batch_data : list
        An array of each batches coordinate found in the form of
        [{index: int, x1: double, y1: double, x2: double, y2: double}...]
    """
    # Use to remove noises (Stray Chips / Dirt)
    img_height, img_width = img_shape
    thres_area = img_height * img_width * 0.01

    batch_data = []

    contours, _ = cv2.findContours(mask_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        ((_, _), (wi, he), _) = cv2.minAreaRect(cnt)
        blob_area = wi * he

        if blob_area > thres_area:
            x, y, w, h = cv2.boundingRect(cnt)
            xc, yc = x + w / 2, y + h / 2

            # Factor depends on the size of image (RoundUp)
            factor = -(-img_height // 1000) * 1000
            index = round(yc / factor, 1) * factor**2 + xc
            data = {"index": index, "x1": x, "y1": y, "x2": x + w, "y2": y + h}
            batch_data.append(data)

    batch_data = sorted(batch_data, key=lambda x: x["index"])

    return batch_data


def find_batch_no(x, y, batch_data):
    """
    Parameters
    ----------
    x : float
        x coordinate of interest point
    y : float
        y coordinate of interest point
    batch_data : list
        An array of each batches coordinate found in the form of
        [{index: int, x1: double, y1: double, x2: double, y2: double}...]

    Returns
    -------
    batch_no
        The batch number the interest is associated with
    """
    batch_no = 0
    for i, coor in enumerate(batch_data):
        if x <= coor["x2"] and x >= coor["x1"] and y <= coor["y2"] and y >= coor["y1"]:
            batch_no = i + 1

    return batch_no
