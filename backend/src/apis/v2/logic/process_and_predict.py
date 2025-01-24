from sqlalchemy.orm import Session
from pathlib import Path
from fastapi import UploadFile
from apis.v2.components.cache_checker import get_cache_if_exists
from apis.v2.components.image_process import process_csam_image
from apis.v2.components.write_images import (
    save_original_image,
    thread_write_temp_images,
)
from apis.v2.schemas.base import CAIPage, CDCPage
from apis.v2.schemas.files import DefectBatchDirectory
from db.models.chip_lot_details import ChipLotDetails
from db.services.chip_details import ChipDetailsService
from db.services.chip_lot_details import ChipLotDetailsService
from schemas.chips_data import DefectBatch, ImageData
from utils.debug import timer
from utils.prediction.tensorflow import TFPrediction


@timer("Process and Predict")
def process_and_predict(
    page: CAIPage | CDCPage, item: str, lot_no: str, file: UploadFile, db: Session
) -> DefectBatchDirectory:
    """Process images, run prediction, and save lot details to the database."""
    plate_no = Path(file.filename).stem
    base_partial_path = f"{page.base_folder}/{item}/{lot_no}/{plate_no}"

    cache_results = get_cache_if_exists(db, lot_no, plate_no, page, base_partial_path)
    if cache_results is not None:
        return cache_results

    image = save_original_image(file, base_partial_path)
    defect_batch_dict, images_to_predict, processed_defects = process_csam_image(
        image, item, lot_no, plate_no
    )

    lot_details = {
        "item": item,
        "lot_no": lot_no,
        "plate_no": plate_no,
        "with_ai": page.ai,
        "no_of_chips": len(images_to_predict) + len(processed_defects),
        "no_of_batches": (
            len(defect_batch_dict) - 1
            if "Stray" in defect_batch_dict.keys()
            else len(defect_batch_dict)
        ),
    }

    if page.ai:
        processed_defects.extend(run_tensorflow(item, images_to_predict))
        lot_details["no_of_pred"] = len(processed_defects)
    else:
        processed_defects.extend(images_to_predict)

    thread_write_temp_images(base_partial_path, processed_defects)
    filtered_batches = filter_defect_data(defect_batch_dict, processed_defects)

    chip_lot_details = write_to_db(db, lot_details, filtered_batches)

    return DefectBatchDirectory(
        unique_id=chip_lot_details.id,
        directory=base_partial_path,
        defect_batches=filtered_batches,
    )


@timer("Run TensorFlow Prediction")
def run_tensorflow(item: str, to_predict_list: list[ImageData]) -> list[ImageData]:
    """Runs TensorFlow predictions on the given list of images."""
    tf_prediction = TFPrediction(item)
    return tf_prediction.run_model_CNN(to_predict_list)


@timer("Filter Defect Data")
def filter_defect_data(
    defect_batch_dict: dict[str, DefectBatch],
    defect_list: list[ImageData],
) -> list[DefectBatch]:
    """Filters defect data, saves chip details to the database, and prepares the response."""

    defect_file_names = {defect.file_name for defect in defect_list}

    updated_batches = [
        defect_batch
        for defect_batch in defect_batch_dict.values()
        if any(
            defect_data.file_name in defect_file_names
            for defect_data in defect_batch.defect_files
        )
    ]

    return sorted(
        updated_batches,
        key=lambda x: (0, int(x.batch_no)) if x.batch_no.isdigit() else (1, x.batch_no),
    )


@timer("Writing to Database")
def write_to_db(
    db: Session, lot_details: dict, filtered_batches: list[DefectBatch]
) -> ChipLotDetails:
    """Writes lot and chip details to the database."""
    chip_lot_detail_service = ChipLotDetailsService(db)
    chip_lot_detail = chip_lot_detail_service.create_lot_details(lot_details)

    bulk_chip_details = [
        {
            **defect_data.__dict__,
            "chip_lot_id": chip_lot_detail.id,
            "batch_no": filtered_defects.batch_no,
        }
        for filtered_defects in filtered_batches
        for defect_data in filtered_defects.defect_files
    ]

    chip_detail_service = ChipDetailsService(db)
    chip_detail_service.create_chip_details(bulk_chip_details)

    return chip_lot_detail
