import requests

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
    item = None
    if lot_no.lower()[:4] == "test":
        item = settings.ITEM
    else:
        prass = requests.get(settings.PRASS_URL + lot_no).json()
        if prass[settings.LOT_COL]:
            item = prass[settings.ITEM_COL]
    return item
