from concurrent.futures import ThreadPoolExecutor
import os
from apis.utils.process import initialize, process, write_image
from apis.utils.debug import time_print
from apis.utils.directory import dire
from apis.utils.cache import get_cache
from apis.CAI.utils.predict_ng import prediction


def CAI(lot_no, file, db=False):

    start = time_print("Received file to process")

    image, item, plate_path, temp_path = initialize(lot_no, file, dire.cai_path)

    lap = time_print("Initialization", start)

    if os.path.isdir(temp_path) and any(os.scandir(temp_path)) and db:
        chip_dict, no_of_chips, no_of_batches = get_cache(plate_path, db)
        return chip_dict, item, plate_path, no_of_chips, no_of_batches

    no_of_chips, no_of_batches, temp_dict, ng_dict = process(image, item, True)

    chip_dict = {}
    for i in range(no_of_batches):
        chip_dict[f"{i+1}"] = []

    lap = time_print("Processing Image", lap)

    res = prediction(item, temp_dict)
    ng_dict.update(res)

    lap = time_print("Prediction of defects", lap)

    with ThreadPoolExecutor(10) as exe:
        _ = [
            exe.submit(write_image, chip_dict, temp_path, key, value, True)
            for key, value in ng_dict.items()
        ]

    _ = time_print("Write and return chip batch data", lap, start)

    return chip_dict, item, plate_path, no_of_chips, no_of_batches
