from collections import defaultdict
from sqlalchemy.orm import Session

from apis.v2.helpers.cache_utils import map_folder_files
from apis.v2.schemas.base import CAIPage, CDCPage
from apis.v2.schemas.files import FileDataBatchDirectory
from core.exceptions import CacheError
from core.logging import logger
from db.models.chip_details import ChipDetails
from db.services.chip_lot_details import ChipLotDetailsService
from schemas.chips_data import FileDataBatch, DefectData
from utils.debug import timer


@timer("Get cache if exists")
def get_cache_if_exists(
    db: Session,
    lot_no: str,
    plate_no: str,
    page: CAIPage | CDCPage,
    base_partial_path: str,
) -> FileDataBatchDirectory:
    """Retrieves defect data for a given lot and plate, grouped by batch number."""

    chip_lot_detail_service = ChipLotDetailsService(db)
    chip_lot_details = chip_lot_detail_service.read_lot_details(
        {"lot_no": lot_no, "plate_no": plate_no, "with_ai": page.ai}
    )
    if not chip_lot_details:
        logger.info("Chip Lot Details not found, creating a new data.")
        return None

    result = map_folder_files(base_partial_path)
    if result is None:
        raise CacheError("Images stored previously not found.")

    temp_dict, non_temp_dict = result
    folder_mapping = {**temp_dict, **non_temp_dict}

    chip_details = chip_lot_details.chips
    if not chip_details:
        logger.info("Chip Details not found or number of files don't match.")
        return None
    if len(folder_mapping) != len(chip_details):
        raise CacheError(
            "Number of images stored in folder don't match number stored in DB."
        )

    batch_data = group_chip_details_by_batch(chip_details)

    logger.info(f"uuid: {chip_lot_details.id}")
    return FileDataBatchDirectory(
        directory=base_partial_path,
        unique_id=chip_lot_details.id,
        file_data_batches=[
            FileDataBatch(batch_no=batch_no, data_files=defects)
            for batch_no, defects in batch_data.items()
        ],
    )


@timer("Group chip details by batch")
def group_chip_details_by_batch(
    chip_details: list[ChipDetails],
) -> dict[str, list[DefectData]]:
    batch_data = defaultdict(list)
    for chip_detail in chip_details:
        batch_data[chip_detail.batch_no].append(
            DefectData(
                file_name=chip_detail.file_name,
                norm_x_center=chip_detail.norm_x_center,
                norm_y_center=chip_detail.norm_y_center,
                defect_mode=chip_detail.defect_mode,
            )
        )

    return batch_data
