from fastapi import APIRouter
from fastapi import Depends, Query, Path
from typing import Annotated
from sqlalchemy.orm import Session

from apis.v2.logic.stats_data import get_lot_details_count
from apis.v2.schemas.common import ServerMode
from apis.v2.schemas.stats_data import CountResult, ItemType
from core.config import service_settings
from db.session import get_db
from services.prass import check_lot

router = APIRouter()


@router.get(
    "/item",
    response_model=ItemType,
    summary="Return Item type from PRASS based on lot number provided",
    operation_id="ItemType",
)
def get_item(
    lot_no: Annotated[
        str,
        Query(
            description="Lot Number",
            pattern="[a-zA-Z0-9]{10}",
            examples=[service_settings.TEST_LOT_NO],
        ),
    ],
) -> ItemType:
    item = check_lot(lot_no)
    return ItemType(item=item)


@router.get(
    "/count/{server_mode}",
    response_model=CountResult,
    summary="Return count stored in database.",
    operation_id="CountResult",
)
def get_processed_count(
    server_mode: Annotated[ServerMode, Path(description="Server Mode (CAI or CDC)")],
    lot_details_id: Annotated[
        str,
        Query(
            description="Lot Details UUID",
            examples=["b79f9b94-f5e5-417b-a3aa-2d701064b1a3"],
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> CountResult:

    is_ai = server_mode == ServerMode.CAI
    return get_lot_details_count(lot_details_id, is_ai, db)
