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


def get_batch_settings(item: str):
    batch_erode = 2
    batch_close = 27
    return batch_erode, batch_close


def get_chip_settings(item: str):
    chip_erode = 7
    chip_close = 2
    return chip_erode, chip_close


def get_crop_settings(item: str):
    crop = 54
    return crop
