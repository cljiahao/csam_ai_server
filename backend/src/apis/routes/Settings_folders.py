from fastapi import APIRouter, HTTPException

from core.read_json import read_config, write_config


router = APIRouter()


@router.get("/get_folders")
def get_folders():
    fol_dict = read_config("./core/json/settings.json")
    return fol_dict


@router.post("/set_folders")
def set_folders(folders: dict):
    fol_dict = read_config("./core/json/settings.json")
    fol_dict["folders"] = folders
    try:
        write_config("./core/json/settings.json", fol_dict)
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
