from core.directory import directory
from core.exceptions import MissingSettings
from core.logging import logger
from utils.fileHandle.base import read_txt, write_txt


def read_model_txt(item: str) -> dict[str, str]:
    """Read and parse a model text file for label data."""

    file_path = directory.model_dir / f"{item}.txt"
    read_data = read_txt(file_path)

    if not read_data:
        std_out = f"Labels File : {file_path.name} is missing dataset keys."
        logger.error(std_out)
        raise MissingSettings(std_out)

    labels = {}
    for line in read_data:
        strip_txt = line.strip()
        try:
            key, value = strip_txt.split(" ")
            labels[key] = value
        except ValueError:
            std_out = f"Labels File: {file_path.name} has an invalid format at line: {strip_txt}."
            logger.error(std_out)
            raise MissingSettings(std_out)

    return labels


def write_model_txt(item: str, write_data: list[str]) -> str:
    """Write list data to a model text file, one item per line, prefixed with an index."""

    file_path = directory.model_dir / f"{item}.txt"

    # Format the write_data into a string with index
    txt_str = "\n".join(f"{i} {data}" for i, data in enumerate(write_data))

    # Write the formatted string to the file
    write_txt(file_path, txt_str)

    return txt_str
