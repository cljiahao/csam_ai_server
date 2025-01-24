from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import File, Depends, Path
from fastapi import APIRouter, UploadFile

from apis.v2.helpers.HTTPExceptions import handle_exceptions
from apis.v2.helpers.pages import get_page
from apis.v2.logic.process_and_predict import process_and_predict
from apis.v2.logic.update_cache import set_cache
from apis.v2.schemas.base import Module
from apis.v2.schemas.files import DefectBatchDirectory
from db.session import get_db

router = APIRouter()

# TODO: implement pagination in the future


@router.post(
    "/image/{module}/{item}/{lot_no}",
    response_model=DefectBatchDirectory,
    summary="Process Image and return chip data",
    operation_id="UploadFile",
)
def process_image(
    module: Module,
    item: Annotated[
        str,
        Path(
            description="Item Type",
            example="GCM32ER71E106KA57",
        ),
    ],
    lot_no: Annotated[
        str,
        Path(
            description="Lot Number",
            pattern="[a-zA-Z0-9]{10}",
            example="1234567890",
        ),
    ],
    file: Annotated[
        UploadFile,
        File(
            description="Upload image file ('.jpg','.png')",
            example="test.png",
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> DefectBatchDirectory:
    """Processes an uploaded image and returns defect batch data."""
    try:
        page = get_page(module)
        return process_and_predict(page, item, lot_no, file, db)
    except Exception as e:
        handle_exceptions(e)


@router.post(
    "/save",
    summary="Update local database with new user input",
    operation_id="SaveLocal",
)
def save_local(
    defect_batch_directory: DefectBatchDirectory,
    db: Session = Depends(get_db),
) -> bool:

    try:
        set_cache(db, defect_batch_directory)
        return True
    except Exception as e:
        handle_exceptions(e)


# TODO: change to API endpoint for receiving file transfer (Model and txt file)


# @router.post(
#     "/settings",
#     summary="Process Image and return chip data",
#     operation_id="UploadSettings",
# )
# def upload_settings(
#     file: UploadFile = File(description="Upload settings.json file."),
# ) -> bool:

#     logger.info(f"{file.filename} uploaded")
#     try:
#         update_settings(file.file, file.filename)
#         return True
#     except Exception as e:
#         handle_exceptions(e)


# @router.post(
#     "/zip",
#     summary="Process Image and return chip data",
#     operation_id="UploadZip",
# )
# def upload_zip(
#     file: UploadFile = File(
#         description="Upload zip file with settings.json and optional, model h5 and txt files."
#     ),
# ) -> bool:

#     logger.info(f"{file.filename} uploaded")
#     try:
#         unzip_files(file.file)
#         return True
#     except Exception as e:
#         handle_exceptions(e)
