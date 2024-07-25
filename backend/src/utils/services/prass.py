import os
import requests
from fastapi import HTTPException

from core.config import settings
from core.logging import logger


def check_lot(lot_no: str) -> str | None:
    """Check if Lot Number input exists in PRASS database"""

    if lot_no.lower()[:4] == "test":
        return settings.TEST_ITEM

    if not settings.PRASS_URL:
        return

    prass = requests.get(settings.PRASS_URL + lot_no).json()
    if not prass[settings.LOT_COL]:
        std_out = f"Lot number: {lot_no} not found in PRASS Server"
        logger.error(std_out)
        raise ValueError(std_out)

    item = prass[settings.ITEM_COL]

    logger.debug("Lot : %s - Item : %s", lot_no, item)

    return item


# TODO: Error checking for HTTP


def via_http(file_path: str) -> None:
    """To Send via HTTP"""

    files = {"file": open(file_path, "rb")}
    resp = requests.post(settings.REALTIMEDB, files=files)

    print(
        f"File Size from server: {int(resp.content)}, Actual File Size: {os.stat(os.path.join(file_path)).st_size}"
    )

    if int(resp.content) != os.stat(os.path.join(file_path)).st_size:
        raise HTTPException(
            status_code=540,
            detail=f"File did not send to file server.",
        )
