import os

from utils.fileHandle.base import read_txt
from core.directory import directory
from core.exceptions import MissingSettings


def read_model_txt(item: str):

    file_name = f"{item}.txt"
    file_path = os.path.join(directory.model_dir, file_name)
    data = read_txt(file_path)

    if not len(data):
        raise MissingSettings("Labels File : {file_name} missing dataset keys.")

    labels = {}
    for x in data:
        res = x.split("\n")[0].split(" ")

        if len(x) != 2:
            raise MissingSettings("Labels File : {file_name} format is wrong.")

        labels[res[0]] = res[1]

    return labels


# TODO: Write text


def write_text(
    file_path: str, data: str | dict, delimiter: str = ",", kv_mode: bool = False
):

    key_val = read_txt(file_path) if os.path.exists(file_path) else {}

    if isinstance(data, dict):
        key_val.update(data)

    txt_str = ""
    if kv_mode:
        for k, v in key_val.items():
            txt_str += f"{k}{delimiter}{v}{delimiter}"
    else:
        for v in key_val.values():
            txt_str += f"{v}{delimiter}"

    with open(file_path, "w") as f:
        f.write(txt_str[:-1])
