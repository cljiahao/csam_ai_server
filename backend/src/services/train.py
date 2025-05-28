import requests
import urllib.parse
from pathlib import Path


from apis.v2.schemas.csam_image import FileDataBatchDirectory
from constants.folder_names import CSAMImageFolderName
from core.config import service_settings
from core.directory_manager import directory_manager as dm
from services.base import APIClient
from utils.debug import error_handler

API_IMAGE_SETTINGS_ENDPOINT = "/api/v2/image_settings"
API_PROCESS_IMAGE_ENDPOINT = "/api/v2/csam_image/process_image"
API_HEALTH_CHECK_ENDPOINT = "/api/v2/health"


@error_handler()
def get_image_settings(item: str) -> dict[str, str] | None:

    api_client = APIClient(service_settings.AI_TRAIN_URL)
    search_params = urllib.parse.urlencode({"item": item})
    try:
        image_settings = api_client.get(
            f"{API_IMAGE_SETTINGS_ENDPOINT}?{search_params}"
        )
        return image_settings
    except requests.RequestException as e:
        return None


@error_handler()
def post_image_file(
    item: str,
    lot_no: str,
    defect_batch_directory: FileDataBatchDirectory,
) -> int:

    api_client = APIClient(service_settings.AI_TRAIN_URL)
    base_directory = defect_batch_directory.directory
    file_name = Path(defect_batch_directory.directory).name
    original_path = dm.images_dir / base_directory / CSAMImageFolderName.ORIGINAL
    file_path_list = {"file": original_path / f"{file_name}.png"}
    data = {
        "item": item,
        "lot_no": lot_no,
        "defect_batch_directory": defect_batch_directory.model_dump_json(),
    }
    image_results = api_client.post_files(
        API_PROCESS_IMAGE_ENDPOINT, file_path_list=file_path_list, data=data
    )
    return image_results


@error_handler()
def train_health_check() -> bool:

    api_client = APIClient(service_settings.AI_TRAIN_URL)
    health_res = api_client.get(API_HEALTH_CHECK_ENDPOINT)
    return bool((health_res or {}).get("status") == "OK")
