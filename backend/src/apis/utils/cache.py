import os
from concurrent.futures import ThreadPoolExecutor
from shutil import copyfile, move

from apis.utils.directory import dire
from apis.utils.process import update_chip_dict
from core.read_write import read_json
from db.repository.cai_ratio import get_ratio


def get_cache(plate_path, db):

    lot_no, plate_no = plate_path.split(os.sep)[-2:]
    no_of_batches, no_of_chips = check_local_db(lot_no, plate_no, db)

    chip_dict = {}
    for i in range(no_of_batches):
        chip_dict[f"{i+1}"] = []

    folders = os.listdir(plate_path)
    folders.remove("original")
    for folder in folders:
        file_path = os.path.join(plate_path, folder)
        with ThreadPoolExecutor(10) as exe:
            _ = [
                exe.submit(update_chip_dict, chip_dict, file_name)
                for file_name in os.listdir(file_path)
            ]

    return chip_dict, no_of_batches, no_of_chips


def set_cache(item, directory, selected):

    if not any([x.values() for x in list(selected.values())]):
        return

    holder = {}

    folders = os.listdir(directory)
    folders.remove("original")
    for fol in folders:
        for os_file in os.listdir(os.path.join(directory, fol)):
            holder[os_file[1:]] = {
                "os_fol": fol,
                "directory": os.path.join(directory, fol, os_file),
            }

    folder_set = list(
        read_json(os.path.join(dire.json_path, "folders.json"))[item].keys()
    )

    for key, value in selected.items():
        dest = os.path.join(directory, key)
        if not os.path.exists(dest):
            os.makedirs(dest)
        for fname in value.values():
            _fname = fname[1:]
            mode = 0 if key not in folder_set else folder_set.index(key) + 1
            new_fname = f"{mode}{_fname}"
            move(
                holder[_fname]["directory"],
                os.path.join(dest, new_fname),
                copy_function=copyfile,
            )
            holder.pop(_fname)

    for k, v in holder.items():
        if v["os_fol"] == "temp":
            continue
        move(
            v["directory"],
            os.path.join(directory, "temp", f"0{k}"),
            copy_function=copyfile,
        )
    return


def check_local_db(lot_no, plate_no, db):
    ratio = get_ratio(lot_no, plate_no, db)
    no_of_batches = ratio.batches
    no_of_chips = ratio.chips

    return no_of_batches, no_of_chips
