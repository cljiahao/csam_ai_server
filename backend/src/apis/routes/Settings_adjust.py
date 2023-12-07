from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from core.read_json import read_config, write_config
from apis.Settings.main import set_upload


router = APIRouter()


class Res(BaseModel):
    chip_type: str


@router.get("/get_settings")
def get_settings():
    set_dict = read_config("./core/json/adjust.json")
    return set_dict


@router.post("/set_settings")
def set_settings(settings: dict):
    try:
        write_config("./core/json/adjust.json", settings)
        alert = {
            "title": "Folders Settings Saved",
            "text": "Confirm to Continue",
            "icon": "success",
            "confirmButtonText": "Confirm",
        }
    except:
        alert = {
            "title": "Folders Failed to Save!",
            "text": "Please Try Again",
            "icon": "error",
            "confirmButtonText": "Confirm",
        }
    return alert


@router.post("/ini_settings")
async def ini_settings(res: Res):
    print("Received file to process, please wait...")
    set_dict = read_config("./core/json/adjust.json")
    if res.chip_type not in set_dict:
        set_dict[res.chip_type] = {
            "batch": {
                "threshold": 1,
                "close_x": 1,
                "close_y": 1,
                "erode_x": 1,
                "erode_y": 1,
            },
            "chip": {
                "threshold": 1,
                "close_x": 1,
                "close_y": 1,
                "erode_x": 1,
                "erode_y": 1,
            },
        }
        write_config("./core/json/adjust.json", set_dict)
