import os
from shutil import rmtree


class Directory:
    src_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    base_path = os.path.dirname(src_path)

    conf_path = os.path.join(base_path, "conf")
    json_path = os.path.join(conf_path, "json")
    model_path = os.path.join(conf_path, "model")

    data_path = os.path.join(base_path, "data")
    image_path = os.path.join(data_path, "images")
    data_send_path = os.path.join(data_path, "datasend")
    cdc_path = os.path.join(image_path, "CDC")
    cai_path = os.path.join(image_path, "CAI")


dire = Directory


def check_dir(lot_no, plate_path):
    temp_path = os.path.join(plate_path, "temp")
    if os.path.isdir(plate_path):
        if lot_no.lower()[:4] == "test":
            rmtree(plate_path)
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    return temp_path
