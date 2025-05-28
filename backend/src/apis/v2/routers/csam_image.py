import shutil
import tempfile
from fastapi import APIRouter, Response, status, UploadFile
from fastapi import Depends, File, Path, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Annotated

from apis.v2.components.cache_image import set_cache_data
from apis.v2.logic.csam_image import process_and_predict
from apis.v2.schemas.common import ServerMode
from apis.v2.schemas.csam_image import FileDataBatchDirectory
from core.config import service_settings
from core.directory_manager import directory_manager as dm
from db.session import get_db
from services.train import post_image_file, train_health_check

router = APIRouter()


@router.post(
    "/process_image/{server_mode}",
    response_model=FileDataBatchDirectory,
    summary="Process image and return predicted defective chip data",
    operation_id="PredictedDefects",
)
def start_process_image(
    server_mode: Annotated[ServerMode, Path(description="Server Mode (CAI or CDC)")],
    item: Annotated[
        str, Query(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
    lot_no: Annotated[
        str,
        Query(
            description="Lot Number (Alphanumeric, 10 characters)",
            pattern="[a-zA-Z0-9]{10}",
            examples=[service_settings.TEST_LOT_NO],
        ),
    ],
    file: Annotated[
        UploadFile,
        File(description="Upload image file ('.jpg','.png')"),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_path = tmp_file.name  # Store the file path

    is_ai = int(server_mode == ServerMode.CAI)
    return process_and_predict(item, lot_no, file.filename, tmp_path, is_ai, db)


@router.get(
    "/{src:path}",
    summary="Return image data",
    operation_id="ImageSource",
)
def get_image(
    src: Annotated[
        str,
        Path(
            description="Path to the image file relative to the image directory",
            pattern=".*\.(png|jpg)$",
        ),
    ],
) -> FileResponse:
    file_path = dm.images_dir / src
    if not file_path.exists():
        raise FileNotFoundError(f"Image file not found: {src}")
    return FileResponse(file_path)


@router.post(
    "/save_local/{server_mode}",
    summary="Update local database with new user input",
    operation_id="SaveLocal",
    status_code=status.HTTP_204_NO_CONTENT,
)
def save_local(
    server_mode: Annotated[ServerMode, Path(description="Server Mode (CAI or CDC)")],
    item: Annotated[
        str, Query(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
    lot_no: Annotated[
        str,
        Query(
            description="Lot Number",
            pattern="[a-zA-Z0-9]{10}",
            examples=[service_settings.TEST_LOT_NO],
        ),
    ],
    defect_batch_directory: FileDataBatchDirectory,
    db: Session = Depends(get_db),
) -> Response:

    if train_health_check():
        post_image_file(server_mode.value, item, lot_no, defect_batch_directory)
    set_cache_data(defect_batch_directory, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
