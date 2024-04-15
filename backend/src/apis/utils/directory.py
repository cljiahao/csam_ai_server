import os
from shutil import rmtree


class Directory:
    src_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    base_path = os.path.dirname(src_path)

    data_path = os.path.join(base_path, "data")
    image_path = os.path.join(data_path, "images")
    data_send_path = os.path.join(data_path, "datasend")
    cdc_path = os.path.join(image_path, "CDC")
    cai_path = os.path.join(image_path, "CAI")
    json_path = os.path.join(src_path, "core", "json")
    model_path = os.path.join(src_path, "core", "model")


dire = Directory


def check_dir(lot_no, plate_path, cache=False):
    temp_path = os.path.join(plate_path, "temp")
    if os.path.isdir(plate_path):
        if lot_no.lower()[:4] == "test" or cache:
            rmtree(plate_path)
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    return temp_path
