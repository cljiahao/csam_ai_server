import io
import os
import json
from typing import BinaryIO
from zipfile import ZipFile
from shutil import copyfileobj

from core.exceptions import MissingSettings
from core.config import settings
from core.directory import directory
from core.logging import logger


def unzip_files(file: BinaryIO):
    """Unzip files and store them into settings and model folders"""

    with ZipFile(io.BytesIO(file.read()), "r") as zipf:
        # Get a list of filenames in zip file
        name_list = zipf.namelist()
        # Check for correct files in zip
        zip_file_exists(name_list)

        for file_name in name_list:
            if file_name == settings.SETTINGS_FNAME:
                update_settings(zipf.open(file_name), file_name)
            else:
                update_model(zipf, file_name)


def zip_file_exists(name_list: list):
    """Check if file is correct format in zip file"""

    if settings.SETTINGS_FNAME not in name_list:
        raise FileNotFoundError(f"{settings.SETTINGS_FNAME} not found in Zip File.")

    model_list = [fname for fname in name_list if fname != settings.SETTINGS_FNAME]

    if len(model_list):
        holder = {}
        for file_name in model_list:
            f_name, ext = os.path.splitext(file_name)
            if f_name not in holder:
                holder[f_name] = []
            holder[f_name].append(ext)

        for value in holder.values():
            if len(value) != 2 and value != settings.MODEL_EXT:
                raise ValueError("Some files in zip file does not match requirement.")


def update_model(zipf: ZipFile, file_name: str):
    """Update model folder with new uploaded models"""

    base_path = os.path.join(directory.model_dir)
    zipf.extract(file_name, base_path)

    logger.info("Extracted %s", file_name)


def update_settings(file: BinaryIO, file_name: str):
    """Update settings file with new uploaded file"""

    check_settings_format(file)
    file.seek(0)

    file_path = os.path.join(directory.json_dir, file_name)
    with open(file_path, "wb+") as f:
        copyfileobj(file, f)

    logger.info("Extracted %s", file_name)


def check_settings_format(file: BinaryIO):
    """Check if uploaded new settings file matches current configuration"""

    data = json.load(file)

    for key, value in data.items():
        for val in value.values():
            if [
                "erode",
                "close",
            ] != list(val) or [
                "batch",
                "chip",
            ] != list(value):
                std_out = f"{key} in Settings file missing some key configuration."
                logger.error(std_out, exc_info=True)
                raise MissingSettings(std_out)
