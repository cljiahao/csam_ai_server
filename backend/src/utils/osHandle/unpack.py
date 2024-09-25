import io
import json
from pathlib import Path
from typing import BinaryIO
from zipfile import ZipFile
from shutil import copyfileobj

import core.constants as core_consts
import utils.osHandle.constants as osHandle_constants
from core.exceptions import MissingSettings
from core.directory import directory
from core.logging import logger


# TODO: Update the zipping and uploading settings, please do pytest for this.


def unzip_files(file: BinaryIO):
    """Unzip files and store them into settings and model folders."""

    with ZipFile(io.BytesIO(file.read()), "r") as zipf:
        # Get a list of filenames in zip file
        name_list = zipf.namelist()
        # Check for correct files in zip
        zip_file_exists(name_list)

        for file_name in name_list:
            if file_name == core_consts.SETTINGS_FILENAME:
                with zipf.open(file_name) as settings_file:
                    update_settings(settings_file, file_name)
            else:
                update_model(zipf, file_name)


def zip_file_exists(name_list: list[str]):
    """Check if file is correct format in zip file."""

    if core_consts.SETTINGS_FILENAME not in name_list:
        std_out = f"{core_consts.SETTINGS_FILENAME} not found in Zip File."
        logger.error(std_out)
        raise FileNotFoundError(std_out)

    model_list = [
        fname for fname in name_list if fname != core_consts.SETTINGS_FILENAME
    ]

    if model_list:
        holder = {}
        for file_name in model_list:
            f_name, ext = Path(file_name).stem, Path(file_name).suffix
            if f_name not in holder:
                holder[f_name] = []
            holder[f_name].append(ext)

        for extensions in holder.values():
            if len(extensions) != 2 and sorted(extensions) != sorted(
                osHandle_constants.MODELS_EXT
            ):
                std_out = f"Some files in zip file does not match requirement."
                logger.error(std_out)
                raise ValueError(std_out)


def update_model(zipf: ZipFile, file_name: str):
    """Update model folder with new uploaded models."""

    zipf.extract(file_name, directory.model_dir)
    logger.info("Extracted %s", file_name)


def update_settings(file: BinaryIO, file_name: str):
    """Update settings file with new uploaded file."""

    check_settings_format(file)
    file.seek(0)

    file_path = directory.json_dir / file_name
    with open(file_path, "wb+") as f:
        copyfileobj(file, f)

    logger.info("Extracted %s", file_name)


def check_settings_format(file: BinaryIO):
    """Check if uploaded new settings file matches current configuration."""

    data = json.load(file)

    required_keys = {"erode", "close"}
    required_sections = {"batch", "chip"}

    for key, value in data.items():
        if not required_sections.issubset(value.keys()) or not all(
            required_keys.issubset(v.keys()) for v in value.values()
        ):
            std_out = f"{key} in Settings file missing some key configuration."
            logger.error(std_out)
            raise MissingSettings(std_out)
