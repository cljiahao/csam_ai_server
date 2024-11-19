import io
import json
from pathlib import Path
from typing import BinaryIO, List
from zipfile import ZipFile
from shutil import copyfileobj

import core.constants as core_consts
from core.exceptions import MissingSettings
from core.directory import directory
from core.logging import logger
from utils.fileHandle.json import validate_settings_format


MODELS_EXT: List[str] = [".h5", ".txt"]


def log_and_raise(exception_class, message: str) -> None:
    """Log an error message and raise an exception."""
    logger.error(message)
    raise exception_class(message)


def unzip_files(file: BinaryIO) -> None:
    """Unzip files and store them into settings and model folders."""
    with ZipFile(io.BytesIO(file.read()), "r") as zipf:
        name_list = zipf.namelist()
        model_list = zip_file_exists(name_list)

        with zipf.open(core_consts.SETTINGS_FILENAME) as settings_file:
            update_settings(settings_file)

        for file_name in model_list:
            update_model(zipf, file_name)


def zip_file_exists(name_list: List[str]) -> None:
    """Check if the required files are present in the zip file."""
    if core_consts.SETTINGS_FILENAME not in name_list:
        log_and_raise(
            FileNotFoundError, f"{core_consts.SETTINGS_FILENAME} not found in Zip File."
        )

    model_list = [
        fname for fname in name_list if fname != core_consts.SETTINGS_FILENAME
    ]
    if model_list:
        holder = {}
        for file_name in model_list:
            f_name, ext = Path(file_name).stem, Path(file_name).suffix
            holder.setdefault(f_name, []).append(ext)

        for extensions in holder.values():
            if len(extensions) != 2 or sorted(extensions) != sorted(MODELS_EXT):
                log_and_raise(
                    ValueError, "Some files in the zip file do not match requirements."
                )

    return model_list


def update_model(zipf: ZipFile, file_name: str) -> None:
    """Update model folder with new uploaded models."""
    zipf.extract(file_name, directory.model_dir)
    logger.info(f"Extracted {file_name}")


def update_settings(
    file: BinaryIO, file_name: str = core_consts.SETTINGS_FILENAME
) -> None:
    """Update settings file with new uploaded file."""

    check_settings_format(file, file_name)
    file.seek(0)

    file_path = directory.json_dir / file_name
    with open(file_path, "wb+") as f:
        copyfileobj(file, f)

    logger.info(f"Extracted {file_name}")


def check_settings_format(file: BinaryIO, file_name: str) -> None:
    """Check if the uploaded settings file matches current configuration."""

    if file_name != core_consts.SETTINGS_FILENAME:
        log_and_raise(
            FileNotFoundError,
            f"{file_name} must be named {core_consts.SETTINGS_FILENAME}.",
        )

    read_data = json.load(file)
    settings_group = read_data.get("settingsGroup", [])

    for item_settings in settings_group:
        item = item_settings["item"]
        settings = item_settings["settings"]

        std_out = validate_settings_format(settings)
        if std_out:
            log_and_raise(MissingSettings, f"Item : {item} {std_out}")
