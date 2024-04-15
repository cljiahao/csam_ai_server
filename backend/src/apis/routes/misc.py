import os
from shutil import move
from zipfile import ZipFile
from fastapi import File
from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse

from apis.utils.directory import dire
from core.read_write import read_json, write_json
from schemas.misc import FolderColor


router = APIRouter()


@router.get("/get_image/{src:path}")
def get_image(src: str):
    file_path = os.path.join(dire.image_path, src)
    return FileResponse(file_path)


@router.post("/get_fol_color")
def get_fol_color(fol_col: FolderColor):
    folder_set = read_json("./core/json/folders.json")[fol_col.item]
    return folder_set


@router.post("/set_fol_color")
def set_fol_color(fol_col: FolderColor):
    folder_set = read_json("./core/json/folders.json")
    folder_set[fol_col.item] = fol_col.color
    write_json("./core/json/folders.json", folder_set)


@router.post("/unzip_files")
def unzip_files(file: UploadFile = File(...)):
    try:
        with ZipFile(file.file, "r") as zipf:
            zipf.extractall(dire.model_path)
    except:
        return False
    if "settings.json" not in os.listdir(dire.model_path):
        return False
    move(
        os.path.join(dire.model_path, "settings.json"),
        os.path.join(dire.json_path, "settings.json"),
    )
    return True
