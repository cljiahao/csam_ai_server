import re

from apis.v2.schemas.defects import CategoryHex
import core.constants as core_consts
from core.directory import directory
from core.exceptions import MissingSettings
from core.logging import logger
from utils.fileHandle.base import read_json, write_json


SETTINGS_JSON_PATH = directory.json_dir / core_consts.SETTINGS_FILENAME
COLORS_JSON_PATH = directory.json_dir / core_consts.COLOR_GROUP_FILENAME


def log_and_raise(error_message: str) -> None:
    """Log an error message and raise a MissingSettings exception."""
    logger.error(error_message)
    raise MissingSettings(error_message)


# Settings Json
def validate_settings_format(
    settings: dict[str, dict[str, list[int, int]]]
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

        invalid_lists = [
            k
            for k, value in settings[key].items()
            if not (
                isinstance(value, list)
                and len(value) == 2
                and all(isinstance(v, int) for v in value)
            )
        ]
        if invalid_lists:
            return f"have invalid lists for keys: {', '.join(invalid_lists)} in key: {key}."

    return None


def read_settings_json() -> list[dict[str, str | dict[str, list[int, int]]]] | list:
    """Retrieve the settings for a specific item from the settings JSON file."""

    read_data = read_json(SETTINGS_JSON_PATH)
    return read_data.get("settingsGroup", [])


def get_settings_json(item: str) -> dict[str, dict[str, list[int, int]]]:
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
    settings_data: dict[str, dict[str, list[int, int]]] = core_consts.DEFAULT_SETTINGS,
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

    write_json(SETTINGS_JSON_PATH, {"settingsGroup": settings_group})


# Colors Json
def validate_colors_hex(colors: list[dict[str, str]]) -> None:
    """Validate that the provided list contains valid HEX color codes."""
    hex_pattern = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")
    for category_hex in colors:
        if not hex_pattern.match(category_hex.get("hex", "")):
            category_hex["hex"] = "#ffff00"
            logger.info("Invalid HEX Code format received.")

    return colors


def read_colors_json() -> list[dict[str, str | list[dict[str, str]]]]:
    """Retrieve the color group data from the colors JSON file."""
    read_data = read_json(COLORS_JSON_PATH)
    return read_data.get("colorGroup", [])


def get_colors_json(item: str) -> list[dict[str, str]]:
    """Retrieve and validate color data for a given item."""

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
        # Validate colors data
        colors = validate_colors_hex(colors)

    return colors


def write_colors_json(item: str, colors_data: CategoryHex) -> None:
    """Write color data for a given item to the colors JSON file."""

    color_group = read_colors_json()

    colors = validate_colors_hex(colors_data)

    updated = False
    for item_data in color_group:
        if item_data["item"] == item:
            item_data["colors"] = colors
            updated = True
            break

    if not updated:
        color_group.append({"item": item, "colors": colors})

    write_json(COLORS_JSON_PATH, {"colorGroup": color_group})


def get_all_colors_json() -> list[dict[str, str | list[dict[str, str]]]]:
    """Retrieve and validate all color data from the colors JSON file."""

    color_group = read_colors_json()
    color_group = [item_data for item_data in color_group if "item" in item_data]

    # Validate all colors data
    for item_data in color_group:
        item_data = validate_colors_hex(item_data.get("colors", []))

    return color_group


def write_all_colors_json(
    colors_group_data: list[dict[str, str | list[dict[str, str]]]]
) -> None:
    """Write and validate all color data to the colors JSON file."""

    # Validate each item in the list
    for item_data in colors_group_data:
        if "item" not in item_data:
            log_and_raise("Item type missing in colors json file.")
        item_data = validate_colors_hex(item_data.get("colors", []))

    write_json(COLORS_JSON_PATH, {"colorGroup": colors_group_data})
