import os
import cv2
import math
import numpy as np

from core.config import settings


def save_original(file, plate_path):
    file_name = file.filename
    np_img = np.asarray(bytearray(file.file.read()))
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    ori_dir = os.path.join(plate_path, "original")
    if not os.path.exists(ori_dir):
        os.makedirs(ori_dir)
    else:
        no_of_files = len(os.listdir(ori_dir))
        archive_name = f"{file_name.split('.')[0]}_{no_of_files}.png"
        os.rename(os.path.join(ori_dir, file_name), os.path.join(ori_dir, archive_name))
    cv2.imwrite(os.path.join(ori_dir, file_name), image)

    return image


def create_border_img(image):
    """
    Parameters
    ----------
    image : MatLike
        Original Image File

    Returns
    -------
    border_img : MatLike
        Border added image
    border_gray : MatLike
        Gray Image for masking purposes
    """
    # Added border to include chips near the edge of images,
    # allowing better cropping of chips later on
    padx, pady = [math.ceil(x * math.sqrt(2) / 10) * 10 for x in settings.CHIP_IMG_SIZE]
    border_img = cv2.copyMakeBorder(image, pady, pady, padx, padx, cv2.BORDER_REPLICATE)

    img = border_img.copy()
    # Mask for background and convert all to 255 for easier threshold (remove background)
    background = np.where(
        (img[:, :, 0] >= 130) & (img[:, :, 1] >= 130) & (img[:, :, 2] >= 130)
    )
    img[background] = (255, 255, 255)
    border_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return border_img, border_gray
