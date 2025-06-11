import urllib.parse

from core.config import service_settings
from core.exceptions import NoResultsFound
from core.logging import logger
from services.base import APIClient
from utils.debug import error_handler

API_PRASS_ITEM_ENDPOINT = "/data"


@error_handler()
def check_lot(lot_no: str) -> str | None:
    """Check if Lot Number input exists in PRASS database."""

    if lot_no.lower() == service_settings.TEST_LOT_NO:
        return service_settings.TEST_ITEM

    if not service_settings.PRASS_URL:
        logger.info("PRASS URL is not configured.")
        return None

    api_client = APIClient(service_settings.PRASS_URL)
    search_params = urllib.parse.urlencode({"lotNo": lot_no})
    prass_data = api_client.get(f"{API_PRASS_ITEM_ENDPOINT}?{search_params}")

    if not isinstance(prass_data, dict):
        raise NoResultsFound(f"Lot number: {lot_no} not found in PRASS Server.")

    item = prass_data[service_settings.ITEM_COLUMN]
    logger.debug(f"Lot : {lot_no} - Item : {item}")

    return item
