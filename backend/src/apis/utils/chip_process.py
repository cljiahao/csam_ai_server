import cv2
import math
import numpy as np
from PIL import Image

from core.config import settings
from core.read_json import read_config
from apis.utils.batch_process import find_batch_no


def chips(border_img, gray, batch_data, prog, chip_type) -> dict:
    """
    Main function to call sub functions for retrieiving chip data

    Parameters
    ----------
    border_img : MatLike
        Directory to check if files exists
    gray : numpy array
        Gray Image for masking purposes
    batch_data : list
        An array of each batches coordinate found in the form of
        [{index: int, x1: double, y1: double, x2: double, y2: double}...]
    prog : str
        Program using this function
    chip_type : str
        chip_type associated with lot number

    Returns
    -------
    no_of_chips : int
        Number of chips
    hold_dict : dict
        Images stored in dictionary to be send back to frontend
    """
    no_of_chips = 0
    temp_dict, ng_dict = {}, {}

    x_crop, y_crop = settings.IMAGESIZE
    x_crop_limit = math.ceil(x_crop * math.sqrt(2) / 10) * 10
    y_crop_limit = math.ceil(y_crop * math.sqrt(2) / 10) * 10

    mask = mask_chips(gray, chip_type)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Average contour area of the chips
    # TODO : dynamic changes to the limits
    cArea = np.median([cv2.contourArea(x) for x in contours if cv2.contourArea(x) > 50])
    lower_chip_area = cArea * 0.15
    upper_chip_area = cArea * 3
    lower_def_area = cArea * 0.75
    upper_def_area = cArea * 1.5

    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        ((xc, yc), (w, h), theta) = rect
        chip_area = cv2.contourArea(cnt)

        if lower_chip_area < chip_area < upper_chip_area:
            no_of_chips += 1
            batch = find_batch_no(xc, yc, batch_data)
            padx, pady = [math.ceil(i / 10) * 10 for i in settings.IMAGESIZE]
            # 0 first element of name is to indicate image not selected yet
            # xc, yc - 20 to remove the the added borders previously
            fName = "{}_{}_{}_{}_{}.png".format(
                0, batch, no_of_chips, int(xc - padx), int(yc - pady)
            )

            rotated_img = rotate_chips(border_img, rect, x_crop_limit, y_crop_limit)
            # Convert colour to RGB for AI Model to predict properly
            if prog == "CAI":
                rotated_img = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2RGB)

            # Reduce predicting data to quicken processing time
            # Chips below certain threshold are considered defects
            if chip_area < lower_def_area or upper_def_area < chip_area:
                ng_dict[fName] = rotated_img
            else:
                temp_dict[fName] = rotated_img

    return no_of_chips, temp_dict, ng_dict


def mask_chips(gray, chip_type):
    """
    Parameters
    ----------
    gray : numpy array
        Gray Image for masking purposes
    chip_type : str
        chip_type associated with lot number

    Returns
    -------
    mask : MatLike
        A masked image of individual chips
    """
    adjust_chip = read_config("./core/json/adjust.json")[chip_type]["chip"]

    th, ret = cv2.threshold(gray, adjust_chip["threshold"], 255, cv2.THRESH_BINARY_INV)
    morph = cv2.morphologyEx(
        ret, cv2.MORPH_CLOSE, (adjust_chip["close_x"], adjust_chip["close_y"])
    )
    mask = cv2.erode(
        morph, np.ones((adjust_chip["erode_x"], adjust_chip["erode_y"]), np.uint8)
    )

    return mask


def rotate_chips(src, rect, x_crop_limit, y_crop_limit):
    """
    Parameters
    ----------
    src : numpy array
        Image to mask out background
    rect: RotatedRect
        Box2D structure containing center(x,y), width, height and angle of rotation
    x_crop_limit: int
        Preliminary x crop limit for final cropping after rotation
    y_crop_limit: int
        Preliminary y crop limit for final cropping after rotation

    Returns
    -------
    rot_img
        Rotated image based on reference point (src_pts and dst_pts)
    """
    x_crop, y_crop = settings.IMAGESIZE
    ((x, y), (width, height), theta) = rect
    if height < width:
        theta = theta - 90

    crop = src[
        int(y - y_crop_limit) : int(y + y_crop_limit),
        int(x - x_crop_limit) : int(x + x_crop_limit),
    ]
    img = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)

    rot_img = im_pil.rotate(theta)
    rot_img = np.asarray(rot_img)
    rot_img = cv2.cvtColor(rot_img, cv2.COLOR_RGB2BGR)
    rot_img = rot_img[
        int(y_crop_limit - y_crop / 2) : int(y_crop_limit + y_crop / 2),
        int(x_crop_limit - x_crop / 2) : int(x_crop_limit + x_crop / 2),
    ]

    return rot_img
