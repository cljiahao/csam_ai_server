from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import File, Depends, Query, Path
from fastapi import APIRouter, UploadFile

from apis.v2.helpers.HTTPExceptions import handle_exceptions
from apis.v2.helpers.pages import get_page
from apis.v2.logic.model_files import save_model_files
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
    server_mode: Annotated[ServerMode, Path(description="")],
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


@router.post(
    "/install_model", summary="Install model received.", operation_id="InstallModel"
)
def install_model(
    item: Annotated[
        str, Query(description="Item Type", examples=["GCM32ER71E106KA57"])
    ],
    file_model_label: Annotated[
        UploadFile,
        File(description="Upload model label file ('.txt')"),
    ],
    file_model: Annotated[
        UploadFile,
        File(description="Upload model file ('.h5','.onnx')"),
    ],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        save_model_files(item, file_model_label, file_model, db)
        return True
    except Exception as e:
        handle_exceptions(e)
