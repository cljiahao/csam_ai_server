from pathlib import Path

from core.directory import directory
from core.exceptions import MissingSettings
from core.logging import logger
from utils.fileHandle.base import read_txt


def read_model_txt(item: str):
    """Read and parse a model text file for label data."""
    file_path = directory.model_dir / f"{item}.txt"
    read_data = read_txt(file_path)

    if not read_data:
        std_out = f"Labels File : {file_path.name} is missing dataset keys."
        logger.error(std_out)
        raise MissingSettings(std_out)

    labels = {}
    for line in read_data:

        try:
            key, value = line.strip().split(" ")
            labels[key] = value
        except ValueError:
            std_out = f"Labels File : {file_path.name} format is wrong."
            logger.error(std_out)
            raise MissingSettings(std_out)

    return labels


# TODO: Write text


def write_text(
    file_path: str, write_data: str | dict, delimiter: str = ",", kv_mode: bool = False
):
    """Write text data to a file, optionally in key-value mode with a delimiter."""

    file_path = Path(file_path)
    key_val = {}

    if file_path.exists():
        key_val = dict(read_txt(file_path))

    if isinstance(write_data, dict):
        key_val.update(write_data)
    else:
        key_val = {i: v for i, v in enumerate(write_data.split(delimiter), start=1)}

    if kv_mode:
        txt_str = delimiter.join([f"{k}{delimiter}{v}" for k, v in key_val.items()])
    else:
        txt_str = delimiter.join(key_val.values())

    with file_path.open("w") as f:
        f.write(txt_str)
