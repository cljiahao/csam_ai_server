import requests


from core.config import service_settings
from core.logging import logger


def get_item_settings(item: str) -> dict | None:
    try:
        response = requests.get(service_settings + item)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        std_out = f"Error fetching settings from train server: {e}"
        print(std_out)
        logger.error(std_out)
        raise
