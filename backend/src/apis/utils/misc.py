import requests
from fastapi import HTTPException

from core.config import settings


def check_lot(lot_no):
    """
    Parameters
    ----------
    lot_no : str
        Lot number keyed in by user

    Returns
    -------
    item : str
        item associated with lot number
    """
    item = ""
    if lot_no.lower()[:4] == "test":
        item = settings.TEST_ITEM
    else:
        if settings.PRASS_URL:
            prass = requests.get(settings.PRASS_URL + lot_no).json()
            if prass[settings.LOT_COL]:
                item = prass[settings.ITEM_COL]
            else:
                raise HTTPException(
                    status_code=521,
                    detail=f"Lot number: {lot_no} not found in database",
                )
    return item
