import requests
from pathlib import Path

from apis.v2.schemas.files import FileDataBatchDirectory
from constants.folder_names import FolderNames
from core.config import service_settings
from core.directory_manager import directory_manager as dm
from services.base import APIClient


def get_image_settings(item: str) -> dict[str, str]:

    api_client = APIClient(service_settings.AI_TRAIN_URL)
    try:
        image_settings = api_client.get(f"/api/v2/settings/image?item={item}")
        return image_settings
    except requests.RequestException as e:
        return None


def post_image_file(
    item: str,
    lot_no: str,
    defect_batch_directory: FileDataBatchDirectory,
):

    api_client = APIClient(service_settings.AI_TRAIN_URL)
    try:
        image_file_name = Path(defect_batch_directory.directory).name
        original_path = (
            dm.images_dir
            / defect_batch_directory.directory
            / FolderNames.ORIGINAL.value
        )
        file_path_list = {
            "file": original_path / f"{image_file_name}.png",
        }
        data = {
            "item": item,
            "lot_no": lot_no,
            "defect_batch_directory": defect_batch_directory.model_dump_json(),
        }
        image_results = api_client.post_files(
            "/api/v2/image/process_image", file_path_list=file_path_list, data=data
        )
        return image_results
    except requests.RequestException as e:
        raise Exception(f"Failed to post model files: {e}")


def train_health_check():

    api_client = APIClient(service_settings.AI_TRAIN_URL)
    try:
        health_res = api_client.get("/api/v2/health")
        return bool((health_res or {}).get("status") == "OK")
    except requests.RequestException as e:
        return None
