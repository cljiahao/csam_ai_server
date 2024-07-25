import cv2
import math
import numpy as np

from core.config import settings
from core.logging import logger
from utils.debug import time_print
from utils.fileHandle.json import get_settings_json
from utils.imgProcess.batch_process import get_batch
from utils.imgProcess.chip_process import get_chips


def img_process(image: cv2.typing.MatLike, item: str, ai: bool = False):
    """Process image to return indiivdual chip images"""

    start, stdout = time_print("Start Processing Image")
    logger.info(stdout)

    try:
        set_data = get_settings_json(item)
    except Exception as e:
        logger.error(e.args[0], exc_info=True)
        raise

    b_img, b_gray = create_border_img(image)

    lap, stdout = time_print("Creating border image and border gray image", start)
    logger.info(stdout)

    batch_data = get_batch(b_gray, set_data["batch"])

    lap, stdout = time_print("Retrieving image batches", lap)
    logger.info(stdout)

    no_of_chips, temp_dict, ng_dict = get_chips(
        b_img, b_gray, batch_data, set_data["chip"], ai
    )

    lap, stdout = time_print("Processing individual chips", lap)
    logger.info(stdout)
    _, stdout = time_print(lap=start, end=True)
    logger.info(stdout)

    count_dict = {
        "no_of_chips": no_of_chips,
        "no_of_batches": len(batch_data),
        "no_of_real": 0,
    }

    return count_dict, temp_dict, ng_dict


def create_border_img(image: cv2.typing.MatLike):
    """Return border extended MatLike image in BGR and Gray"""

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
