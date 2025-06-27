import requests

# from pathlib import Path

from core.config import service_settings
from core.logging import logger
from services.base import APIClient


def check_lot(lot_no: str) -> str | None:
    """Check if Lot Number input exists in PRASS database."""

    if lot_no.lower() == service_settings.TEST_LOT_NO:
        return service_settings.TEST_ITEM

    if not service_settings.PRASS_URL:
        logger.info("PRASS URL is not configured.")
        return

    api_client = APIClient(service_settings.PRASS_URL)
    prass_data = api_client.get(lot_no)

    if not prass_data[service_settings.LOT_COLUMN]:
        raise ValueError(f"Lot number: {lot_no} not found in PRASS Server.")

    item = prass_data[service_settings.ITEM_COLUMN]
    logger.debug("Lot : %s - Item : %s", lot_no, item)

    return item


# def via_http(file_path: str) -> None:
#     """To Send via HTTP."""

#     file_path = Path(file_path)
#     with file_path.open("rb") as file:
#         files = {"file": file}
#         response = requests.post(database_settings.REALTIMEDB, files=files)
#         response.raise_for_status()  # Raise HTTPError for bad responses

#     server_file_size = int(response.content)
#     actual_file_size = file_path.stat().st_size

#     if server_file_size != actual_file_size:
#         raise ValueError(
#             "File size mismatch. File may not have been uploaded correctly."
#         )

#     logger.info(
#         "File sent successfully. Server reported file size: %d", server_file_size
#     )
