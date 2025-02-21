import requests

from core.config import ServiceSettings
from core.logging import logger
from db.models.image_settings import ImageSettings
from services.base import APIClient


def get_image_settings(item: str) -> ImageSettings:

    api_client = APIClient(ServiceSettings.AI_TRAIN_URL)
    try:
        image_settings = api_client.get(item)
        return image_settings
    except requests.RequestException as e:
        return None
