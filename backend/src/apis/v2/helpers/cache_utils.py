from pathlib import Path

from core.directory import directory
from core.logging import logger
from schemas.chips_data import DefectData


def map_folder_files(base_partial_path: str) -> dict[str, Path] | None:
    """Maps file names to their respective folder paths, ignoring 'original' folder."""
    plate_path = directory.images_dir / base_partial_path
    if not plate_path.exists() or not plate_path.is_dir():
        return None

    temp_dict, non_temp_dict = {}, {}
    for folder in plate_path.iterdir():
        if not folder.is_dir() or folder.name == "original":
            continue
        target_dict = temp_dict if folder.name == "temp" else non_temp_dict
        target_dict.update(
            {file.name: folder for file in folder.iterdir() if file.is_file()}
        )

    return temp_dict, non_temp_dict


def get_non_temp_changes(
    defect_files: list[DefectData],
    chip_detail_dict: dict[str, DefectData],
    folder_mapping: dict[str, Path],
) -> list[DefectData]:
    """Finds changes in non-temp defect files."""
    return [
        defect_file
        for defect_file in defect_files
        if defect_file.file_name not in chip_detail_dict
        or defect_file.file_name not in folder_mapping
        or defect_file.defect_mode
        != chip_detail_dict[defect_file.file_name].defect_mode
    ]


def get_temp_changes(
    defect_files: list[DefectData],
    chip_detail_dict: dict[str, DefectData],
    non_temp_dict: dict[str, Path],
) -> list[DefectData]:
    """Finds changes in temp defect files."""
    defect_file_names = {defect_file.file_name for defect_file in defect_files}
    temp_changes = []
    for non_temp_file_name in non_temp_dict:
        if non_temp_file_name not in defect_file_names:
            defect_data = chip_detail_dict.get(non_temp_file_name)
            defect_data.defect_mode = "temp"
            temp_changes.append(defect_data)

    return temp_changes


def move_file(source_folder: Path, defect: DefectData) -> None:
    """Moves a single defect file to the defect mode folder."""
    destination_folder = source_folder.parent / defect.defect_mode
    destination_folder.mkdir(parents=True, exist_ok=True)
    source_file = source_folder / defect.file_name

    if source_file.exists():
        destination_file = destination_folder / defect.file_name
        source_file.rename(destination_file)
        logger.info(f"Moved {defect.file_name} to {destination_file}")
    else:
        logger.info(f"File {defect.file_name} not found in {source_folder}")


def count_defects(base_partial_path: str) -> int:
    """Counts the valid defect files excluding 'original' and 'temp' folders."""
    plate_path = directory.images_dir / base_partial_path
    if not plate_path.exists() or not plate_path.is_dir():
        return 0
    return sum(
        len([file for file in folder.iterdir() if file.is_file()])
        for folder in plate_path.iterdir()
        if folder.is_dir() and folder.name not in ["original", "temp"]
    )
