import numpy as np
from collections import defaultdict
from pathlib import Path
from sqlalchemy.orm import Session

from apis.v2.components.cache_image import get_cache_data
from apis.v2.components.model_prediction import run_model_prediction
from apis.v2.components.process_batch import (
    create_batch_contour_info_list,
    find_batch_no,
    get_batch_data_from_contour_info,
)
from apis.v2.components.process_chips import (
    create_chip_contour_info_list,
    deform_chip_condition,
    rotate_and_crop_chip_image,
)
from apis.v2.components.utils_image_process import convert_white_bg_to_gray_to_binary
from apis.v2.components.write_images import (
    save_original_image,
    thread_write_temp_images,
)
from apis.v2.schemas.common import ServerMode
from apis.v2.schemas.csam_image import (
    DefectData,
    FileDataBatch,
    FileDataBatchDirectory,
    LabeledImageData,
)
from constants.folder_names import CSAMImageFolderName
from db.models.image_settings import ImageSettings
from db.services.image_settings import ImageSettingsService
from db.services.lot_details import LotDetailsService
from services.train import get_image_settings
from utils.debug import timer
from utils.image_process.border_creator import BorderCreator
from utils.misc.calculations import calculate_border_padding, normalize_coordinates


@timer("Process and Predict")
def process_and_predict(
    item: str, lot_no: str, file_name: str, file_path: str, is_ai: int, db: Session
):

    page = ServerMode.CAI if bool(is_ai) else ServerMode.CDC
    plate_no = Path(file_name).stem
    base_partial_path = f"{page}/{item}/{lot_no}/{plate_no}"

    cache_results = get_cache_data(lot_no, plate_no, is_ai, base_partial_path, db)
    if cache_results is not None:
        return cache_results

    image = save_original_image(file_name, file_path, base_partial_path)
    to_predict_image_datas, deform_image_datas = process_csam_image(
        item, lot_no, plate_no, image, db
    )
    no_of_chips = len(to_predict_image_datas + deform_image_datas)

    lot_details = {
        "item": item,
        "lot_no": lot_no,
        "plate_no": plate_no,
        "is_ai": is_ai,
        "no_of_chips": no_of_chips,
    }

    if is_ai:
        predicted_defect_images = run_model_prediction(item, to_predict_image_datas)
        deform_image_datas.extend(predicted_defect_images)
        lot_details["no_of_pred"] = len(deform_image_datas)
    else:
        deform_image_datas.extend(to_predict_image_datas)

    thread_write_temp_images(base_partial_path, deform_image_datas)
    batch_file_data = group_defect_data_by_batch(deform_image_datas)

    lot_details["no_of_batches"] = (
        len(batch_file_data) - 1
        if "Stray" in [batch_data.batch_no for batch_data in batch_file_data]
        else len(batch_file_data)
    )

    lot_details_id = write_new_lot_to_db(batch_file_data, lot_details, db)

    return FileDataBatchDirectory(
        unique_id=lot_details_id,
        directory=base_partial_path,
        file_data_batches=batch_file_data,
    )


@timer("Processing CSAM Image")
def process_csam_image(
    item: str, lot_no: str, plate_no: str, image: np.ndarray, db: Session
) -> tuple[list[LabeledImageData], list[LabeledImageData]]:
    """Processes a single CSAM image to identify and classify chips."""
    image_settings = get_or_fetch_image_settings(item, db)
    crop_size = image_settings.crop_size

    border_padding = calculate_border_padding(crop_size)
    border_image = BorderCreator.create_border_image(image, border_padding)
    binary_image = convert_white_bg_to_gray_to_binary(border_image)
    base_file_name = f"{lot_no}_{plate_no}"

    batch_contour_infos = create_batch_contour_info_list(binary_image, image_settings)
    batch_data = get_batch_data_from_contour_info(border_image, batch_contour_infos)

    black_refined_contour_infos, non_black_refined_contour_infos, chip_threshold = (
        create_chip_contour_info_list(border_image, binary_image, image_settings)
    )
    chip_contour_infos = black_refined_contour_infos + non_black_refined_contour_infos

    non_deform_data_list = []
    deform_data_list = []
    for i, contour_info in enumerate(chip_contour_infos, start=1):
        coordinates = contour_info.rect[0]
        batch_no = find_batch_no(batch_data, coordinates)
        norm_coords = normalize_coordinates(
            coordinates, border_image.shape[:2], border_padding
        )

        rotated_image = rotate_and_crop_chip_image(
            contour_info, border_image, border_padding, crop_size
        )

        label_image_data = LabeledImageData(
            batch_no=batch_no,
            file_name=f"{base_file_name}_{i}.png",
            image_data=rotated_image,
            norm_x_center=norm_coords.norm_x,
            norm_y_center=norm_coords.norm_y,
        )
        if deform_chip_condition(chip_threshold, contour_info):
            non_deform_data_list.append(label_image_data)
        else:
            deform_data_list.append(label_image_data)

    return non_deform_data_list, deform_data_list


@timer("Get Image Settings")
def get_or_fetch_image_settings(item: str, db: Session) -> ImageSettings:
    json_image_settings = get_image_settings(item)  # External API call

    image_settings_service = ImageSettingsService(db)
    if json_image_settings is not None:
        image_settings = image_settings_service.create_or_update_image_settings(
            item, json_image_settings
        )
        return image_settings
    # Fall back to local database if API fails and returns None
    return image_settings_service.read_image_settings_not_empty(item)


@timer("Grouping DefectData by Batch")
def group_defect_data_by_batch(
    image_data_list: list[LabeledImageData],
) -> list[FileDataBatch]:
    batch_to_defect_data = defaultdict(list)
    for i, image_data in enumerate(image_data_list):
        batch_to_defect_data[image_data.batch_no].append(
            DefectData(
                id=str(i),
                norm_x_center=image_data.norm_x_center,
                norm_y_center=image_data.norm_y_center,
                file_name=image_data.file_name,
                defect_mode=CSAMImageFolderName.TEMP,
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


@timer("Writing New Lot To Database")
def write_new_lot_to_db(
    chip_details_data: list[FileDataBatch], lot_details: dict, db: Session
):

    bulk_chip_details = [
        {
            **defect_data.__dict__,
            "batch_no": filtered_defects.batch_no,
        }
        for filtered_defects in chip_details_data
        for defect_data in filtered_defects.defect_records
    ]

    lot_details_service = LotDetailsService(db)
    lot_details_id = lot_details_service.bulk_create_lot_and_chip_details(
        bulk_chip_details, lot_details
    )

    return lot_details_id
