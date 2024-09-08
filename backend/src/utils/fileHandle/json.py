import re

import core.constants as core_consts
from core.directory import directory
from core.exceptions import MissingSettings
from core.logging import logger
from utils.fileHandle.base import read_json, write_json


COLORS_JSON_PATH = directory.json_dir / core_consts.SETTINGS_FILENAME
COLORS_JSON_PATH = directory.json_dir / core_consts.COLOR_GROUP_FILENAME


def log_and_raise(error_message: str) -> None:
    """Log an error message and raise a MissingSettings exception."""
    logger.error(error_message)
    raise MissingSettings(error_message)


# Settings Json
def validate_settings_format(
    settings: dict[str, dict[str, tuple[int, int]]]
) -> str | None:
    """Validate the format of the settings data."""

    for key in core_consts.SETTINGS_TYPE:
        if key not in settings:
            return f"missing key: {key}."

        missing_sub_keys = [
            k for k in core_consts.SETTINGS_MODE if k not in settings[key]
        ]
        if missing_sub_keys:
            return f"missing sub-keys: {', '.join(missing_sub_keys)} in key: {key}."

        invalid_tuples = [
            k
            for k, value in settings[key].items()
            if not (
                isinstance(value, tuple)
                and len(value) == 2
                and all(isinstance(v, int) for v in value)
            )
        ]
        if invalid_tuples:
            return f"have invalid tuples for keys: {', '.join(invalid_tuples)} in key: {key}."

    return None


def read_settings_json() -> dict[str, dict[str, tuple[int, int]]] | None:
    """Retrieve the settings for a specific item from the settings JSON file."""

    read_data = read_json(COLORS_JSON_PATH)
    return read_data.get("settingsGroup", [])


def get_settings_json(item: str) -> dict[str, dict[str, tuple[int, int]]]:
    """Retrieve and validate settings for a specific item from the settings JSON file."""

    settings_group = read_settings_json()
    settings = next(
        (
            item_data["settings"]
            for item_data in settings_group
            if item_data["item"] == item
        ),
        None,
    )

    if not settings:
        log_and_raise(f"Item : {item} not found in settings file.")

    # Validate settings data
    std_out = validate_settings_format(settings)
    if std_out:
        log_and_raise(f"Item : {item} {std_out}")

    return settings


def write_settings_json(
    item: str,
    settings_data: dict[str, dict[str, tuple[int, int]]] = core_consts.DEFAULT_SETTINGS,
) -> None:
    """Write settings data for a specific item to the settings JSON file."""

    settings_group = read_settings_json()

    std_out = validate_settings_format(settings_data)
    if std_out:
        log_and_raise(f"Item : {item} {std_out}")

    # Update or append the settings
    updated = False
    for item_data in settings_group:
        if item_data["item"] == item:
            item_data["settings"] = settings_data
            updated = True
            break

    if not updated:
        settings_group.append({"item": item, "settings": settings_data})

    write_json(COLORS_JSON_PATH, {"settingsGroup": settings_group})


# Colors Json
def validate_colors_hex(fol_hex_array: list[dict[str, str]]) -> None:
    """Validate that the provided list contains valid HEX color codes."""
    hex_pattern = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")
    for fol_hex in fol_hex_array:
        if not hex_pattern.match(fol_hex.get("hex", "")):
            log_and_raise("Invalid HEX Code format received.")


def read_colors_json() -> list[dict[str, str | list[dict[str, str]]]]:
    """Retrieve the color group data from the colors JSON file."""
    read_data = read_json(COLORS_JSON_PATH)
    return read_data.get("colorGroup", [])


def get_colors_json(item: str) -> list[dict[str, str | list[dict[str, str]]]]:
    """Retrieve color data from the colors JSON file. Optionally filter by item."""

    color_group = read_colors_json()

    # Check if the item exists in the colorGroup
    colors = next(
        (item_data["colors"] for item_data in color_group if item_data["item"] == item),
        [],
    )
    if not colors:
        logger.info(f"Item : {item} not found in colors file.")
        colors = core_consts.DEFAULT_COLORS
    else:
        validate_colors_hex(colors)

    return colors


def write_colors_json(
    fol_hex_data: list[dict[str, str | list[dict[str, str]]]], item: str
) -> None:
    """Write color data to the colors JSON file. Optionally filter by item."""

    color_group = read_colors_json()

    validate_colors_hex(fol_hex_data)

    updated = False
    for item_data in color_group:
        if item_data["item"] == item:
            item_data["colors"] = fol_hex_data
            break

    if not updated:
        color_group.append({"item": item, "colors": fol_hex_data})

    write_json(COLORS_JSON_PATH, {"colorGroup": color_group})


def get_all_colors_json() -> list[dict[str, str | list[dict[str, str]]]]:
    """Retrieve color data from the colors JSON file. Optionally filter by item."""

    color_group = read_colors_json()

    # TODO: add the missing colors or revert to proper hex?
    # Validate colors data
    for item_data in color_group:
        validate_colors_hex(item_data.get("colors", []))
        if "item" not in item_data:
            log_and_raise("Item type missing in colors json file.")

    return color_group


def write_all_colors_json(
    fol_hex_data: list[dict[str, str | list[dict[str, str]]]]
) -> None:
    """Write color data to the colors JSON file. Optionally filter by item."""

    # Validate each item in the list
    for item_data in fol_hex_data:
        validate_colors_hex(item_data.get("colors", []))
        if "item" not in item_data:
            log_and_raise("Item type missing in colors json file.")

    write_json(COLORS_JSON_PATH, {"colorGroup": fol_hex_data})
