from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Body, Depends, Query
from fastapi import APIRouter

from apis.v2.helpers.HTTPExceptions import handle_exceptions
from apis.v2.logic.dot_colors import get_dot_colors_by_item, save_dot_colors_by_item
from apis.v2.schemas.colors import ItemDotColors
from db.session import get_db

router = APIRouter()


@router.get(
    "/dotter",
    summary="Return list of Dot Colors based on item type provided",
)
def get_dot_colors(
    item: Annotated[
        str, Query(description="Item Type", examples=["GCM32ER71E106KA57"])
    ],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        return get_dot_colors_by_item(item, db)
    except Exception as e:
        handle_exceptions(e)


@router.post(
    "/dotter",
    summary="Save Dot Colors into local database for retrieval.",
)
def get_dot_colors(
    item_dot_colors: Annotated[
        ItemDotColors, Body(description="List of defect labels and hex colors")
    ],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        save_dot_colors_by_item(item_dot_colors, db)
        return True
    except Exception as e:
        handle_exceptions(e)
