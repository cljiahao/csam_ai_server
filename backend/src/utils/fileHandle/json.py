import os
import re

from core.directory import directory
from core.exceptions import MissingSettings
from core.logging import logger
from utils.fileHandle.base import read_json, write_json


def get_settings_json(item: str):

    file_path = os.path.join(directory.json_dir, "settings.json")
    data = read_json(file_path)

    if item not in data:
        std_out = f"Item : {item} not found in settings file."
        logger.error(std_out, exc_info=True)
        raise MissingSettings(std_out)
    item_set = data[item]

    set_data = {}
    for key in ["batch", "chip"]:
        if key not in item_set or list(item_set[key]) != ["erode", "close"]:
            std_out = f"{key.capitalize()} settings under Item : {item} not found in settings file."
            logger.error(std_out, exc_info=True)
            raise MissingSettings(std_out)
        erode = item_set[key]["erode"]
        close = item_set[key]["close"]

        set_data[key] = {"erode": erode, "close": close}

    return set_data


def write_settings_json(item: str, set_data: dict = {}):

    file_path = os.path.join(directory.json_dir, "settings.json")
    data = read_json(file_path)

    if item not in data:
        data[item] = {}

    for key in ["batch", "chip"]:
        for k in ["erode", "close"]:
            if key not in set_data or k not in set_data[key]:
                std_out = f"{key.capitalize()} settings under Item : {item} not found in settings file."
                logger.error(std_out, exc_info=True)
                raise MissingSettings(std_out)
            data[item][key][k] = set_data[key][k]

    write_json(file_path, data)


def get_folder_json(item: str):

    file_path = os.path.join(directory.json_dir, "folders.json")
    data = read_json(file_path)

    if item not in data:
        data[item] = {"ng": "#ffff00", "others": "#00ffff"}
        write_json(file_path, data)

    return data[item]


def write_folder_json(item: str, fol_data: dict = {}):

    file_path = os.path.join(directory.json_dir, "folders.json")
    data = read_json(file_path)

    if item not in data:
        data[item] = {}

    for key, value in fol_data.items():
        if not re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", value):
            std_out = "Wrong HEX Code format received"
            logger.error(std_out, exc_info=True)
            raise MissingSettings(std_out)
        data[item][key] = value

    write_json(file_path, data)
