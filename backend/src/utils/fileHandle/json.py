import re

import core.constants as core_consts
from core.directory import directory
from core.exceptions import MissingSettings
from core.logging import logger
from utils.fileHandle.base import read_json, write_json

SETTINGS_TYPE = ["batch", "chip"]
SETTINGS_MODE = ["erode", "close"]
DEFAULT_SETTINGS = {
    "batch": {"erode": (1, 1), "close": (1, 1)},
    "chip": {"erode": (1, 1), "close": (1, 1)},
}


def check_settings_format(
    settings: dict[str, dict[str, tuple[int, int]]]
) -> str | None:
    """Validate the format of the settings data."""

    for key in SETTINGS_TYPE:
        if key not in settings:
            return f"missing key: {key}."

        missing_sub_keys = [k for k in SETTINGS_MODE if k not in settings[key]]
        if missing_sub_keys:
            return f"missing sub-keys: {', '.join(missing_sub_keys)} in key: {key}."

        invalid_tuples = [
            k
            for k, value in settings[key].items()
            if not isinstance(value, tuple)
            or len(value) != 2
            or not all(isinstance(v, int) for v in value)
        ]
        if invalid_tuples:
            return f"have invalid tuples for keys: {', '.join(invalid_tuples)} in key: {key}."

    return None


def get_settings_json(item: str) -> dict[str, dict[str, tuple[int, int]]]:
    """Retrieve settings for a specific item from the settings JSON file."""

    file_path = directory.json_dir / core_consts.SETTINGS_FILENAME
    read_data = read_json(file_path)
    settings_data = read_data.get("processSettings", [])

    # Check if the item exists in the settings
    settings = next(
        (
            item_data["settings"]
            for item_data in settings_data
            if item_data["item"] == item
        ),
        None,
    )

    if not settings:
        std_out = "not found in settings file."
    else:
        # Validate and extract settings
        std_out = check_settings_format(settings_data, item)

    if std_out:
        new_std_out = f"Item : {item} {std_out}"
        logger.error(new_std_out)
        raise MissingSettings(new_std_out)

    return {
        key: {
            "erode": settings[key]["erode"],
            "close": settings[key]["close"],
        }
        for key in SETTINGS_TYPE
    }


def write_settings_json(
    item: str, sett_data: dict[str, dict[str, tuple[int, int]]] = DEFAULT_SETTINGS
) -> None:
    """Write settings data for a specific item to the settings JSON file."""

    file_path = directory.json_dir / core_consts.SETTINGS_FILENAME
    read_data = read_json(file_path)
    settings_data = read_data.get("processSettings", [])

    # Validate and extract settings
    std_out = check_settings_format(settings_data, item)
    if std_out:
        new_std_out = f"Item : {item} {std_out}"
        logger.error(new_std_out)
        raise MissingSettings(new_std_out)

    # Update or append the settings
    updated = False
    for item_data in settings_data:
        if item_data["item"] == item:
            item_data["settings"] = sett_data
            updated = True
            break

    if not updated:
        settings_data.append({"item": item, "settings": sett_data})

    write_json(file_path, {"processSettings": settings_data})


def get_colors_json(item: str = None) -> list[dict[str, str | list[dict[str, str]]]]:
    """Retrieve color data from the colors JSON file. Optionally filter by item."""

    file_path = directory.json_dir / core_consts.COLOR_GROUP_FILENAME
    read_data = read_json(file_path)
    colors_data = read_data.get("colorGroup", [])

    if item:
        # Find the entry for the specified item
        entry = next((group for group in colors_data if group["item"] == item), None)
        return entry.get("colors", []) if entry else []

    return colors_data


def write_colors_json(
    fol_hex_data: list[dict[str, str | list[dict[str, str]]]], item: str = None
) -> None:
    """Write color data to the colors JSON file. Optionally filter by item."""

    def check_hex(fol_hex_array):
        """Validate HEX codes in the color data."""
        hex_pattern = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")
        for fol_hex in fol_hex_array:
            if not hex_pattern.match(fol_hex.get("hex", "")):
                std_out = "Invalid HEX Code format received."
                logger.error(std_out)
                raise MissingSettings(std_out)

    file_path = directory.json_dir / core_consts.COLOR_GROUP_FILENAME
    read_data = read_json(file_path)
    colors_data = read_data.get("colorGroup", [])

    if item:
        # TODO: Allow individual add item if don't exist?
        check_hex(fol_hex_data)
        for item_data in colors_data:
            if item_data["item"] == item:
                item_data["colors"] = fol_hex_data
                break

    else:
        # Validate each item in the list
        for item_data in fol_hex_data:
            check_hex(item_data.get("colors", []))
            if "item" not in item_data:
                std_out = "Item type missing in data received."
                logger.error(std_out)
                raise MissingSettings(std_out)

        colors_data = fol_hex_data

    write_json(file_path, {"colorGroup": colors_data})
