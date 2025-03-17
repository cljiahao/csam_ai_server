from pathlib import Path
from sqlalchemy.orm import Session
from apis.v2.helpers.cache_utils import (
    count_defects,
    get_non_temp_changes,
    get_temp_changes,
    map_folder_files,
    move_file,
)
from apis.v2.schemas.files import FileDataBatchDirectory
from core.exceptions import CacheError
from db.services.chip_details import ChipDetailsService
from db.services.chip_lot_details import ChipLotDetailsService
from schemas.chips_data import DefectData
from utils.debug import timer


@timer("Set cache")
def set_cache(db: Session, defect_batch_directory: FileDataBatchDirectory) -> None:
    """Updates the cache by synchronizing defect modes and moving files to respective folders."""
    result = map_folder_files(defect_batch_directory.directory)
    if result is None:
        raise CacheError(f"Folder path: {defect_batch_directory.directory} missing")

    temp_dict, non_temp_dict = result
    folder_mapping = {**temp_dict, **non_temp_dict}
    chip_detail_service = ChipDetailsService(db)
    chip_details = chip_detail_service.read_all_chip_details(
        {"chip_lot_id": defect_batch_directory.unique_id}
    )

    if not chip_details or len(folder_mapping) != len(chip_details):
        raise CacheError("Mismatch between stored chip images and stored chip details.")

    data_files = [
        data_file
        for defect_batch in defect_batch_directory.file_data_batches
        for data_file in defect_batch.data_files
    ]

    chip_detail_dict = {
        chip_detail.file_name: chip_detail for chip_detail in chip_details
    }

    data_changes = get_data_changes(
        data_files, chip_detail_dict, folder_mapping, non_temp_dict
    )
    if not data_changes:
        raise CacheError("No defects to update.")

    update_list = [
        {
            "filter_conditions": {"file_name": defect.file_name},
            "update_data": {"defect_mode": defect.defect_mode},
        }
        for defect in data_changes
    ]

    chip_detail_service.bulk_update_chip_details(update_list)

    move_files_to_defect_mode_folders(data_changes, folder_mapping)

    chip_lot_detail_service = ChipLotDetailsService(db)
    chip_lot_detail_service.update_lot_details(
        {"id": defect_batch_directory.unique_id},
        {"no_of_real": count_defects(defect_batch_directory.directory)},
    )


@timer("Get Data Changes")
def get_data_changes(
    data_files: list[DefectData],
    chip_detail_dict: dict[str, str],
    folder_mapping: dict[str, Path],
    non_temp_dict: dict[str, Path],
) -> list[DefectData]:
    non_temp_changes = get_non_temp_changes(
        data_files,
        chip_detail_dict,
        folder_mapping,
    )
    temp_changes = get_temp_changes(
        data_files,
        chip_detail_dict,
        non_temp_dict,
    )
    return non_temp_changes + temp_changes


@timer("Moving files to correct path")
def move_files_to_defect_mode_folders(
    defect_data: list[DefectData], folder_mapping: dict[str, Path]
) -> None:
    """Move files from the source folder to their respective defect mode folders."""
    for defect in defect_data:
        source_folder = folder_mapping.get(defect.file_name)
        if source_folder:
            move_file(source_folder, defect)
