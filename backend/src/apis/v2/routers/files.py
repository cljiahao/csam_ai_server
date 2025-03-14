from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import File, Depends, Query, Path as FastAPIPath
from fastapi import APIRouter, UploadFile

from apis.v2.helpers.HTTPExceptions import handle_exceptions
from apis.v2.helpers.pages import get_page
from apis.v2.logic.process_and_predict import process_and_predict
from apis.v2.logic.update_cache import set_cache
from apis.v2.schemas.base import ServerMode
from apis.v2.schemas.files import FileDataBatchDirectory
from db.session import get_db

router = APIRouter()

# TODO: implement pagination in the future


@router.post(
    "/process_image/{server_mode}",
    response_model=FileDataBatchDirectory,
    summary="Process Image and return chip data",
    operation_id="UploadFile",
)
def start_process_image(
    server_mode: Annotated[ServerMode, FastAPIPath(description="")],
    item: Annotated[
        str, Query(description="Item Type", examples=["GCM32ER71E106KA57"])
    ],
    lot_no: Annotated[
        str,
        Query(
            description="Lot Number (Alphanumeric, 10 characters)",
            pattern="[a-zA-Z0-9]{10}",
            examples=["1234567890"],
        ),
    ],
    file: Annotated[
        UploadFile,
        File(description="Upload image file ('.jpg','.png')"),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> FileDataBatchDirectory:
    try:

        page = get_page(server_mode)
        return process_and_predict(page, item, lot_no, file, db)
    except Exception as e:
        handle_exceptions(e)


@router.post(
    "/save_local",
    summary="Update local database with new user input",
    operation_id="SaveLocal",
)
def save_local(
    defect_batch_directory: FileDataBatchDirectory,
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
