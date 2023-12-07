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
    chip_type : str
        chip_type associated with lot number
    """
    if lot_no.lower()[:4] == "test":
        chip_type = settings.CHIPTYPE
    else:
        prass = requests.get(settings.PRASS_URL + lot_no).json()
        chip_type = prass["cdc0163"]
        if prass[settings.LOT_NO_COL] == None:
            chip_type = None

    return chip_type
