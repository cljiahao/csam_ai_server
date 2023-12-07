import os
import cv2
import math
import numpy as np

from core.config import settings


def create_border_img(file, save_dir):
    """
    Parameters
    ----------
    file : numpy array
        Image file from frontend
    save_dir : str
        Directory to save folder and files to

    Returns
    -------
    border_img : MatLike
        Border added image
    [w,h] : list
        Width and height of the image
    """
    np_img = np.asarray(bytearray(file.file.read()))
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    ori_dir = os.path.join(save_dir, "original")
    if not os.path.exists(ori_dir):
        os.makedirs(ori_dir)
        cv2.imwrite(os.path.join(ori_dir, file.filename), image)
    else:
        no_of_files = len(os.listdir(ori_dir))
        new_fname = f"{file.filename.split('.')[0]}_{no_of_files}.png"
        os.rename(
            os.path.join(ori_dir, file.filename), os.path.join(ori_dir, new_fname)
        )
        cv2.imwrite(os.path.join(ori_dir, file.filename), image)

    h, w, z = image.shape
    # Added border to include chips near the edge of images,
    # allowing better cropping of chips later on
    padx, pady = [math.ceil(i / 10) * 10 for i in settings.IMAGESIZE]
    border_img = cv2.copyMakeBorder(image, pady, pady, padx, padx, cv2.BORDER_REPLICATE)

    return border_img, [w, h]
