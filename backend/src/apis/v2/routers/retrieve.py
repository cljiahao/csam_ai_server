from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, Path
from fastapi import APIRouter
from fastapi.responses import FileResponse

from apis.v2.helpers.HTTPExceptions import handle_exceptions
from apis.v2.helpers.pages import get_page
from apis.v2.schemas.base import Module
from apis.v2.schemas.retrieve import CountResult, Item
from db.services.chip_lot_details import ChipLotDetailsService
from db.session import get_db
from core.logging import logger
from core.directory import directory
from utils.services.prass import check_lot

router = APIRouter()


@router.get(
    "/item/{lot_no}",
    response_model=Item,
    summary="Return Item type from PRASS based on lot number provided",
)
def get_item(
    lot_no: Annotated[str, Path(description="Lot Number", pattern="[a-zA-Z0-9]{10}")]
):
    try:
        item = check_lot(lot_no)
        return {"item": item}
    except Exception as e:
        handle_exceptions(e)


@router.get(
    "/image/{src:path}",
    summary="Return image data",
)
def get_image(
    src: Annotated[
        str,
        Path(
            description="Path to the image file relative to the image directory",
            pattern=".*\.(png|jpg)$",
        ),
    ]
):
    try:
        file_path = directory.images_dir / src

        if not file_path.exists():
            std_out = f"Image file not found: {src}"
            logger.error(std_out)
            raise FileNotFoundError(std_out)

        return FileResponse(file_path)
    except Exception as e:
        handle_exceptions(e)


@router.get(
    "/count/{module}/{lot_no}/{plate_no}",
    response_model=CountResult,
    summary="Return count stored in database.",
)
def get_processed_count(
    module: Module,
    lot_no: Annotated[str, Path(description="Lot Number", pattern="[a-zA-Z0-9]{10}")],
    plate_no: Annotated[str, Path(description="Plate No")],
    db: Annotated[Session, Depends(get_db)],
):

    try:
        page = get_page(module)
        chip_lot_details_service = ChipLotDetailsService(db)
        filter_condition = {"lot_no": lot_no, "plate_no": plate_no, "with_ai": page.ai}
        lot_detail = chip_lot_details_service.read_lot_details(filter_condition)
        return (
            {"result": lot_detail.no_of_pred}
            if page.ai
            else {"result": lot_detail.no_of_chips}
        )
    except Exception as e:
        handle_exceptions(e)
