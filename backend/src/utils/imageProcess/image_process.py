import numpy as np

from core.logging import logger
from utils.debug import time_print
from utils.fileHandle.json import get_settings_json
from utils.imageProcess.batch_process import get_batch
from utils.imageProcess.chip_process import get_chips
from utils.imageProcess.image_utils import create_border_image


def image_process(
    image: np.ndarray, item: str, ai: bool = False
) -> tuple[dict, dict, dict]:
    """Process image to return indiivdual chip images."""

    _, stdout = time_print("Instantiate settings...")
    logger.info(stdout)

    settings_data = get_settings_json(item)

    start, stdout = time_print("Start Processing Image")
    logger.info(stdout)

    border_image, border_gray = create_border_image(
        image, settings_data["chip"]["crop"]
    )

    lap, stdout = time_print("Creating border image and border gray image", start)
    logger.info(stdout)

    batch_data = get_batch(border_gray, settings_data["batch"])

    lap, stdout = time_print("Retrieving image batches", lap)
    logger.info(stdout)

    no_of_chips, temp_dict, ng_dict = get_chips(
        border_image, border_gray, batch_data, settings_data["chip"], ai
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
