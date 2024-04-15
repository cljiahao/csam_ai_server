import os
import cv2
from fastapi import HTTPException

from apis.utils.misc import check_lot
from apis.utils.image_process import create_border_img, save_original
from apis.utils.batch_process import batch
from apis.utils.debug import time_print
from apis.utils.chip_process import chips
from apis.utils.directory import check_dir
from core.read_write import read_json


def initialize(lot_no, file, base_path):

    item = check_lot(lot_no)
    if not item:
        raise HTTPException(
            status_code=521, detail=f"Lot number: {lot_no} not found in database"
        )
    plate_no = file.filename.split(".")[0]
    plate_path = os.path.join(base_path, item, lot_no, plate_no)

    temp_path = check_dir(lot_no, plate_path)

    image = save_original(file, plate_path)

    return image, item, plate_path, temp_path


def process(image, item, ai=False):

    start = time_print("Processing Image")

    process_set = read_json("./core/json/settings.json")[item]

    b_img, b_gray = create_border_img(image)

    lap = time_print("Creating border image and border gray image", start)

    batch_data = batch(b_gray, image.shape[:2], process_set["batch"])

    lap = time_print("Batching image", lap)

    no_of_chips, temp_dict, ng_dict = chips(b_img, b_gray, batch_data, process_set, ai)

    lap = time_print("Processing individual chips", lap)

    return no_of_chips, len(batch_data), temp_dict, ng_dict


def write_image(chip_dict, temp_path, file_name, img, ai=False):

    if ai:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(os.path.join(temp_path, file_name), img)

    update_chip_dict(chip_dict, file_name)


def update_chip_dict(chip_dict, file_name):

    batch = file_name.split("_")[1]

    if batch != 0:
        chip_dict[batch].append(file_name)
    else:
        if "Stray" not in chip_dict.keys():
            chip_dict["Stray"] = []
        chip_dict["Stray"].append(file_name)
