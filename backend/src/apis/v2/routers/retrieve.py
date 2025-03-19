from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, Path, Query
from fastapi import APIRouter
from fastapi.responses import FileResponse

from apis.v2.helpers.HTTPExceptions import handle_exceptions
from apis.v2.helpers.pages import get_page
from apis.v2.logic.model_files import get_model_history
from apis.v2.schemas.base import ServerMode
from apis.v2.schemas.retrieve import CountResult, Item
from db.services.chip_lot_details import ChipLotDetailsService
from db.session import get_db
from core.directory_manager import directory_manager as dm
from services.prass import check_lot

router = APIRouter()


@router.get(
    "/item",
    response_model=Item,
    summary="Return Item type from PRASS based on lot number provided",
)
def get_item(
    lot_no: Annotated[str, Query(description="Lot Number", pattern="[a-zA-Z0-9]{10}")],
):
    try:
        item = check_lot(lot_no)
        return {"item": item}
    except Exception as e:
        handle_exceptions(e)


@router.get(
    "/count/{server_mode}",
    response_model=CountResult,
    summary="Return count stored in database.",
)
def get_processed_count(
    server_mode: Annotated[ServerMode, Path(description="")],
    lot_no: Annotated[str, Query(description="Lot Number", pattern="[a-zA-Z0-9]{10}")],
    plate_no: Annotated[str, Query(description="Plate No")],
    db: Annotated[Session, Depends(get_db)],
):

    try:
        page = get_page(server_mode)
        chip_lot_details_service = ChipLotDetailsService(db)
        filter_conditions = {
            "lot_no": lot_no,
            "plate_no": plate_no,
            "with_ai": page.is_ai.value,
        }
        lot_detail = chip_lot_details_service.read_lot_details(filter_conditions)
        return (
            {"result": lot_detail.no_of_pred}
            if page.is_ai.value
            else {"result": lot_detail.no_of_chips}
        )
    except Exception as e:
        handle_exceptions(e)


@router.get(
    "/model_history",
    summary="Return count stored in database.",
)
def get_model_history_by_item(
    item: Annotated[
        str, Query(description="Item Type", examples=["GCM32ER71E106KA59_+B55-E02GJ"])
    ],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        return get_model_history(item, db)
    except Exception as e:
        handle_exceptions(e)
