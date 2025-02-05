import requests

# from pathlib import Path

from core.config import service_settings
from core.logging import logger


def check_lot(lot_no: str) -> str | None:
    """Check if Lot Number input exists in PRASS database."""

    if lot_no.lower() == service_settings.TEST_LOT_NO:
        return service_settings.TEST_ITEM

    if not service_settings.PRASS_URL:
        logger.error("PRASS URL is not configured.")
        return

    try:
        response = requests.get(service_settings.PRASS_URL + lot_no)
        response.raise_for_status()
        prass = response.json()
    except requests.RequestException as e:
        std_out = f"Error fetching data from PRASS server: {e}"
        print(std_out)
        logger.error(std_out)
        raise

    if not prass[service_settings.LOT_COLUMN]:
        std_out = f"Lot number: {lot_no} not found in PRASS Server."
        logger.error(std_out)
        raise ValueError(std_out)

    item = prass[service_settings.ITEM_COLUMN]
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
