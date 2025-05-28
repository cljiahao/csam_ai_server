from collections import defaultdict
from pathlib import Path
from sqlalchemy.orm import Session

from apis.v2.schemas.csam_image import DefectData, FileDataBatch, FileDataBatchDirectory
from constants.folder_names import CSAMImageFolderName
from core.directory_manager import directory_manager as dm
from core.exceptions import NoResultsFound
from core.logging import logger
from db.models.chip_details import ChipDetails
from db.services.lot_details import LotDetailsService
from utils.debug import error_handler, timer


@timer("Get Cache Data")
def get_cache_data(
    lot_no: str,
    plate_no: str,
    is_ai: int,
    base_partial_path: str,
    db: Session,
) -> FileDataBatchDirectory:
    """Retrieves cached image defect data from the database and filesystem."""
    lot_details_service = LotDetailsService(db)
    lot_details = lot_details_service.read_lot_details(lot_no, plate_no, is_ai)
    if not lot_details:
        logger.info("Chip Lot Details not found, creating a new data.")
        return None

    plate_path = dm.images_dir / base_partial_path
    file_name_folder_dict = map_file_name_to_folder(plate_path)
    chip_details: list[ChipDetails] = lot_details.chip_details

    validate_image_data_integrity(file_name_folder_dict, chip_details)

    batch_file_data = group_cache_data_by_batch(chip_details)
    return FileDataBatchDirectory(
        unique_id=lot_details.id,
        directory=base_partial_path,
        file_data_batches=batch_file_data,
    )


@timer("Group DefectData by Batch")
def group_cache_data_by_batch(
    chip_details_list: list[ChipDetails],
) -> list[FileDataBatch]:
    """Groups a list of chip details into batches based on their batch number."""
    batch_to_defect_data = defaultdict(list)
    for chip_details in chip_details_list:
        batch_to_defect_data[chip_details.batch_no].append(
            DefectData(
                norm_x_center=chip_details.norm_x_center,
                norm_y_center=chip_details.norm_y_center,
                file_name=chip_details.file_name,
                defect_mode=chip_details.defect_mode,
            )
        )
    file_data_batches = [
        FileDataBatch(batch_no=batch_no, defect_records=defect_data_list)
        for batch_no, defect_data_list in batch_to_defect_data.items()
    ]
    return sorted(
        file_data_batches,
        key=lambda x: (0, int(x.batch_no)) if x.batch_no.isdigit() else (1, x.batch_no),
    )


@timer("Update Cache Data")
def set_cache_data(
    defect_batch_directory: FileDataBatchDirectory,
    db: Session,
) -> None:
    """Updates the chip defect records in the DB based on the given defect batch directory."""
    lot_details_service = LotDetailsService(db)
    lot_details_id = defect_batch_directory.unique_id
    lot_details = lot_details_service.read_lot_details_by_id(lot_details_id)
    if not lot_details:
        raise ValueError("Chip Lot Details not found.")

    plate_path = dm.images_dir / defect_batch_directory.directory
    file_name_folder_map = map_file_name_to_folder(plate_path)
    chip_details: list[ChipDetails] = lot_details.chip_details

    validate_image_data_integrity(file_name_folder_map, chip_details)

    defect_records = [
        defect_record
        for defect_batch in defect_batch_directory.file_data_batches
        for defect_record in defect_batch.defect_records
    ]
    image_data_changes = compute_defect_changes(
        defect_records, file_name_folder_map, chip_details
    )
    if not image_data_changes:
        raise NoResultsFound("No defects to update.")

    move_files_to_defect_mode_folders(image_data_changes, file_name_folder_map)

    lot_details_service.bulk_update_chip_details(image_data_changes)
    lot_details_service.update_lot_details(lot_details_id, len(image_data_changes))


def compute_defect_changes(
    defect_records: list[DefectData],
    file_name_to_folder: dict[str, str],
    chip_details: list[ChipDetails],
) -> list[dict[str, str]]:
    """Returns a list of image data changes for database update"""
    db_file_name_to_mode = {chip.file_name: chip.defect_mode for chip in chip_details}
    new_defect_changes = [
        {"file_name": defect.file_name, "defect_mode": defect.defect_mode}
        for defect in defect_records
        if defect.file_name not in file_name_to_folder
        or defect.file_name not in db_file_name_to_mode
        or defect.defect_mode != db_file_name_to_mode[defect.file_name]
    ]

    defect_record_file_names = {defect.file_name for defect in defect_records}
    revert_defect_changes = [
        {"file_name": file_name, "defect_mode": CSAMImageFolderName.TEMP}
        for file_name, folder in file_name_to_folder.items()
        if folder != CSAMImageFolderName.TEMP
        and file_name not in defect_record_file_names
    ]

    return new_defect_changes + revert_defect_changes


@timer("Moving files to correct path")
def move_files_to_defect_mode_folders(
    defect_data: list[dict[str, str]], file_name_folder_map: dict[str, Path]
) -> None:
    """Move files from the source folder to their respective defect mode folders."""
    for defect in defect_data:
        source_folder = file_name_folder_map.get(defect["file_name"])
        if not source_folder:
            continue

        destination_folder = source_folder.parent / defect["defect_mode"]
        source_file = source_folder / defect["file_name"]
        dm.create_directory(destination_folder)

        if source_file.exists() and not source_folder.samefile(destination_folder):
            destination_file = destination_folder / defect["file_name"]
            source_file.rename(destination_file)
            logger.info(f"Moved {defect['file_name']} to {destination_file}")
        else:
            logger.warning(f"File {defect['file_name']} not found in {source_folder}")


def map_file_name_to_folder(folder_path: Path) -> dict[str, Path]:
    """Maps file names to their respective folder paths, ignoring 'original' folder."""
    if not folder_path.exists() or not folder_path.is_dir():
        return {}

    return {
        file.name: folder
        for folder in folder_path.iterdir()
        if folder != CSAMImageFolderName.ORIGINAL
        for file in folder.iterdir()
        if file.is_file()
    }


@error_handler()
def validate_image_data_integrity(
    file_name_folder_dict: dict[str, Path], chip_details_list: list[ChipDetails]
) -> None:
    """Validates whether chip data from the DB matches the image files present."""
    if not file_name_folder_dict:
        raise NoResultsFound("Images stored previously not found.")

    if not chip_details_list:
        raise NoResultsFound("Chip Details not found.")

    if len(file_name_folder_dict) != len(chip_details_list):
        raise ValueError(
            "Number of images stored in folder don't match number stored in DB."
        )
