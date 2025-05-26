from core.config import service_settings
from core.exceptions import NoResultsFound
from core.logging import logger
from services.base import APIClient
from utils.debug import error_handler


@error_handler()
def check_lot(lot_no: str) -> str | None:
    """Check if Lot Number input exists in PRASS database."""

    if lot_no.lower() == service_settings.TEST_LOT_NO:
        return service_settings.TEST_ITEM

    if not service_settings.PRASS_URL:
        logger.info("PRASS URL is not configured.")
        return None

    api_client = APIClient(service_settings.PRASS_URL)
    prass_data = api_client.get(lot_no)

    if not isinstance(prass_data, dict):
        raise NoResultsFound(f"Lot number: {lot_no} not found in PRASS Server.")

    item = prass_data[service_settings.ITEM_COLUMN]
    logger.debug(f"Lot : {lot_no} - Item : {item}")

    return item
