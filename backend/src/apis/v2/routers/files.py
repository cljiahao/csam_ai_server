from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import File, Depends, Path
from fastapi import APIRouter, UploadFile

from apis.v2.components.process_predict import process_n_predict
from apis.v2.helpers.HTTPExceptions import handle_exceptions
from apis.v2.helpers.pages import get_page
from apis.v2.schemas.base import Module
from apis.v2.schemas.files import ChipData
from core.logging import logger
from db.CRUD.csam import update_lot_detail
from db.session import get_db
from utils.imageCache.cache import set_cache_data
from utils.osHandle.unpack import unzip_files, update_settings


router = APIRouter()


@router.post(
    "/image/{module}/{lot_no}/{item}",
    response_model=ChipData,
    summary="Process Image and return chip data",
    operation_id="UploadFile",
)
def process_image(
    module: Module,
    lot_no: Annotated[str, Path(description="Lot Number", pattern="[a-zA-Z0-9]{10}")],
    item: Annotated[str, Path(description="Item Type")],
    file: Annotated[UploadFile, File(description="Upload image file ('.jpg','.png')")],
    db: Annotated[Session, Depends(get_db)],
) -> ChipData:

    try:
        page = get_page(module)
        res_dict = process_n_predict(lot_no, item, file, db, page)
        return res_dict
    except Exception as e:
        handle_exceptions(e)


@router.post(
    "/save/{module}/{lot_no}/{plate}/{item}",
    summary="Update local database with new user input",
    operation_id="SaveLocal",
)
def save_local(
    module: Module,
    lot_no: Annotated[str, Path(description="Lot Number", pattern="[a-zA-Z0-9]{10}")],
    plate: Annotated[str, Path(description="Plate")],
    item: Annotated[str, Path(description="Item Type")],
    res_dict: ChipData,
    db: Session = Depends(get_db),
) -> bool:

    try:
        page = get_page(module)
        set_cache_data(item, res_dict.directory, res_dict.chips)
        no_of_real = sum(len(value) for value in res_dict.chips.values())
        update_lot_detail(page.model, db, lot_no, plate, no_of_real)
        return True
    except Exception as e:
        handle_exceptions(e)


@router.post(
    "/settings",
    summary="Process Image and return chip data",
    operation_id="UploadSettings",
)
def upload_settings(
    file: UploadFile = File(description="Upload settings.json file."),
) -> bool:

    logger.info(f"{file.filename} uploaded")
    try:
        update_settings(file.file, file.filename)
        return True
    except Exception as e:
        handle_exceptions(e)


@router.post(
    "/zip",
    summary="Process Image and return chip data",
    operation_id="UploadZip",
)
def upload_zip(
    file: UploadFile = File(
        description="Upload zip file with settings.json and optional, model h5 and txt files."
    ),
) -> bool:

    logger.info(f"{file.filename} uploaded")
    try:
        unzip_files(file.file)
        return True
    except Exception as e:
        handle_exceptions(e)
