from fastapi import APIRouter, Response, status
from fastapi import Body, Depends, Query
from sqlalchemy.orm import Session
from typing import Annotated

from apis.v2.logic.color_pick import get_dot_colors_by_item, save_dot_colors_by_item
from apis.v2.schemas.color_pick import ItemDotColors
from core.config import service_settings
from db.session import get_db

router = APIRouter()


@router.get(
    "/dot_colors",
    response_model=ItemDotColors,
    summary="Return list of Dot Colors based on item type provided",
    operation_id="GetDotColor",
)
def get_dot_colors(
    item: Annotated[
        str, Query(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
    db: Annotated[Session, Depends(get_db)],
) -> ItemDotColors:
    return get_dot_colors_by_item(item, db)


@router.post(
    "/dot_colors",
    summary="Save Dot Colors into local database for retrieval.",
    operation_id="SaveDotColors",
    status_code=status.HTTP_204_NO_CONTENT,
)
def get_dot_colors(
    item_dot_colors: Annotated[
        ItemDotColors, Body(description="List of defect labels and hex colors")
    ],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    save_dot_colors_by_item(item_dot_colors, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
