import os
from typing import IO
from pathlib import Path
from sqlalchemy.orm import Session


from apis.v2.schemas.base import CAIPage, CDCPage
from core.directory import directory
from core.logging import logger
from db.CRUD.csam import create_lot_detail, get_lot_detail
from utils.debug import time_print
from utils.imageCache.cache import get_cache_data
from utils.imageProcess.image_process import image_process
from utils.osHandle.initialize import initialize
from utils.osHandle.write_image import thread_write_images
from utils.prediction.tensorflow_model import predict_defects



def process_n_predict(
    lot_no: str, item: str, file: IO, db: Session, page: CAIPage | CDCPage
) -> dict[str, str | dict[str, list[str]]]:
    """
    Main function to run image processing and predictions.

    Parameters:
    - lot_no: The lot number associated with the image.
    - item: The item identifier for the process.
    - file: The image file to be processed.
    - db: Database session for data operations.
    - page: CAIPage or CDCPage object containing page-specific configurations.

    Returns:
    - A dictionary with keys 'chips' containing processed chip data and 'directory' with the relative path.
    """

    start, stdout = time_print(f"Received file to process for {page.base_folder}")
    logger.info(stdout)

    # Initial checks and file saving
    fol_path = directory.images_dir / page.base_folder
    image, plate_path, temp_path = initialize(lot_no, item, file, fol_path)

    res_dict = {
        "chips": {},
        "directory": os.path.relpath(plate_path, directory.images_dir),
    }

    # Read from database if data exists
    plate_no = Path(file.filename).stem
    lot_detail = get_lot_detail(page.model, db, lot_no, plate_no)

    lap, stdout = time_print("Initialization checks", start)
    logger.info(stdout)

    # Check and return if cache data exists
    if list(temp_path.iterdir()) or len(list(plate_path.iterdir())) > 2:
        chip_dict = get_cache_data(lot_detail.no_of_batches, plate_path)
        res_dict["chips"] = chip_dict

        lap, stdout = time_print("Get previously cached data", start)
        logger.info(stdout)
        _, stdout = time_print(lap=start, end=True)
        logger.info(stdout)
        return res_dict

    # Process image to return individual chip images
    count_dict, temp_dict, ng_dict = image_process(image, item, page.ai)

    lap, stdout = time_print("Processing image", start)
    logger.info(stdout)

    if page.ai:
        # Load Model based on item name and run prediction
        pred_dict = predict_defects(item, temp_dict)
        ng_dict.update(pred_dict)

        lap, stdout = time_print("Prediction of defects", start)
        logger.info(stdout)
    else:
        ng_dict.update(temp_dict)

    # Write images to temp path
    chip_dict = thread_write_images(
        count_dict["no_of_batches"], ng_dict, temp_path, page.ai
    )
    res_dict["chips"] = chip_dict

    lap, stdout = time_print("Write and return chip data and directory", lap)
    logger.info(stdout)

    if page.ai:
        # Count number of predictions by AI model
        count_dict["no_of_pred"] = sum(
            len(chip_dict[x]) for x in chip_dict if isinstance(chip_dict[x], list)
        )

    # Save processed initial data into DB if not exists
    if not lot_detail:
        lot_dict = {
            "lotNo": lot_no,
            "plate": plate_no,
            "item": item,
        }

        lot_dict.update(count_dict)
        create_lot_detail(page.model, db, lot_dict)

    lap, stdout = time_print("Write data into database", lap)
    logger.info(stdout)
    _, stdout = time_print(lap=start, end=True)
    logger.info(stdout)

    return res_dict
