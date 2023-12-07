import os
import cv2
import math
import time
import numpy as np

from core.config import settings
from apis.utils.batch_process import mask_batch
from apis.utils.chip_process import mask_chips


def time_print(start, func_name) -> None:
    """
    Parameters
    ----------
    start : float
        Start time from previous recording
    func_name : string
        Description for previous recording
    """
    print(f"{func_name} took: {round(time.time()-start,2)} secs")

    return time.time()


def set_upload(file, uuid):
    np_img = np.asarray(bytearray(file.file.read()))
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    h, w, z = image.shape
    # Added border to include chips near the edge of images,
    # allowing better cropping of chips later on
    padx, pady = [math.ceil(i / 10) * 10 for i in settings.IMAGESIZE]
    border_img = cv2.copyMakeBorder(image, pady, pady, padx, padx, cv2.BORDER_REPLICATE)

    batch_mask = mask_batch(border_img.copy())
    chip_mask = mask_chips(border_img.copy())

    return batch_mask, chip_mask, uuid
