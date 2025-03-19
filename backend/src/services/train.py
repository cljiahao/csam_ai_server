import requests

from core.config import service_settings
from services.base import APIClient


def get_image_settings(item: str) -> dict[str, str]:

    api_client = APIClient(service_settings.AI_TRAIN_URL)
    try:
        image_settings = api_client.get(f"/api/v2/settings/image?item={item}")
        return image_settings
    except requests.RequestException as e:
        return None
