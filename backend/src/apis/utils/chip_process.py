import cv2
import math
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

from core.config import settings
from apis.utils.batch_process import find_batch_no


def chips(b_img, b_gray, batch_data, process_set, ai):
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
    process_set: dict
        Settings used for processing image
    ai : bool
        Program using this function

    Returns
    -------
    no_of_chips : int
        Number of chips
    hold_dict : dict
        Images stored in dictionary to be send back to frontend
    """

    padx, pady = [math.ceil(x * math.sqrt(2) / 10) * 10 for x in settings.CHIP_IMG_SIZE]

    blank = np.zeros(b_img.shape[:2], np.uint8)
    mask = mask_chips(b_gray, process_set["chip"])
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Average contour area of the chips
    thres_range = process_set["thres_range"]
    avg_area = np.median(
        [cv2.contourArea(x) for x in contours if cv2.contourArea(x) > 50]
    )
    low_c_area, upp_c_area, low_def_area, upp_def_area = [
        avg_area * x for x in thres_range.values()
    ]

    no_of_chips = 0
    temp_dict, ng_dict = {}, {}
    with ThreadPoolExecutor(10) as exe:
        for cnt in contours:
            no_of_chips = exe.submit(
                get_chips,
                b_img,
                blank,
                batch_data,
                cnt,
                no_of_chips,
                ng_dict,
                temp_dict,
                low_c_area,
                upp_c_area,
                low_def_area,
                upp_def_area,
                padx,
                pady,
                ai,
            ).result()

    return no_of_chips, temp_dict, ng_dict


def get_chips(
    b_img,
    blank,
    batch_data,
    cnt,
    no_of_chips,
    ng_dict,
    temp_dict,
    low_c_area,
    upp_c_area,
    low_def_area,
    upp_def_area,
    padx,
    pady,
    ai,
):
    if upp_def_area < cv2.contourArea(cnt):
        cnt_arr = check_single(blank.copy(), cnt)
    else:
        cnt_arr = [cnt]
    for c in cnt_arr:
        cArea = cv2.contourArea(c)
        rect = cv2.minAreaRect(c)
        ((xc, yc), _, _) = rect
        if low_c_area < cArea < upp_c_area:
            batch = find_batch_no(xc, yc, batch_data)
            no_of_chips += 1
            # 0 first element of name is to indicate image not selected yet
            # xc, yc - 20 to remove the the added borders previously
            fName = "{}_{}_{}_{}_{}.png".format(
                0, batch, no_of_chips, int(xc - padx), int(yc - pady)
            )

            rotated_img = rotate_chips(b_img, rect, padx, pady)

            # Convert colour to RGB for AI Model to predict properly
            if ai:
                rotated_img = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2RGB)

            # Reduce predict data to quicken processing time
            # Chips below certain threshold are considered defects
            if cArea < low_def_area or upp_def_area < cArea:
                ng_dict[fName] = rotated_img
            else:
                temp_dict[fName] = rotated_img

    return no_of_chips


def mask_chips(gray, set_chip):
    """
    Parameters
    ----------
    gray : numpy array
        Gray Image for masking purposes
    set_chip : dict
        Chip processing Setting information

    Returns
    -------
    mask : MatLike
        A masked image of individual chips
    """

    _, ret = cv2.threshold(gray, set_chip["threshold"], 255, cv2.THRESH_BINARY_INV)
    morph = cv2.morphologyEx(ret, cv2.MORPH_CLOSE, (3, 3))
    erode = cv2.erode(
        morph, np.ones((set_chip["erode_x"], set_chip["erode_y"]), np.uint8)
    )
    mask = cv2.morphologyEx(
        erode,
        cv2.MORPH_CLOSE,
        np.ones((set_chip["close_x"], set_chip["close_y"]), np.uint8),
    )

    return mask


def check_single(blank, cnt):
    """
    Parameters
    ----------
    blank : numpy array
        Blank Image copy for drawing contours on
    contour : MatLike
        Contour of single chip or multi chip
    rect

    Returns
    -------
    cnt_arr: list
        List of contours
    """
    cnt_arr = []
    x_crop, y_crop = settings.CHIP_IMG_SIZE
    ((x, y), _, _) = cv2.minAreaRect(cnt)
    cv2.drawContours(blank, [cnt], -1, (255, 255, 255), -1)
    crop = blank[
        int(y - y_crop / 2) : int(y + y_crop / 2),
        int(x - x_crop / 2) : int(x + x_crop / 2),
    ]
    try:
        crop[:] = cv2.erode(crop, np.ones((9, 9), np.uint8))
        new_cnts, _ = cv2.findContours(
            blank, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
    except:
        new_cnts, _ = cv2.findContours(crop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(new_cnts) > 1:
        for new_c in new_cnts:
            cnt_arr.append(new_c)
    else:
        cnt_arr = new_cnts

    return cnt_arr


def rotate_chips(src, rect, padx, pady):
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
    x_crop, y_crop = settings.CHIP_IMG_SIZE
    ((x, y), (width, height), theta) = rect
    if height < width:
        theta = theta - 90

    crop = src[
        int(y - pady) : int(y + pady),
        int(x - padx) : int(x + padx),
    ]

    img = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)

    rot_img = im_pil.rotate(theta)
    rot_img = np.asarray(rot_img)
    rot_img = cv2.cvtColor(rot_img, cv2.COLOR_RGB2BGR)
    rot_img = rot_img[
        int(pady - y_crop / 2) : int(pady + y_crop / 2),
        int(padx - x_crop / 2) : int(padx + x_crop / 2),
    ]

    return rot_img
