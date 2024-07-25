import io
import os
from shutil import move, copyfileobj
from zipfile import ZipFile
from fastapi import File
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse

from apis.utils.directory import dire
from apis.utils.misc import check_lot
from core.read_write import read_json, write_json
from schemas.misc import CheckItem, FolderColor


router = APIRouter()


@router.post("/get_item")
def get_item(lot_no: CheckItem):
    item = check_lot(lot_no.lot_no)
    return item


@router.get("/get_image/{src:path}")
def get_image(src: str):
    file_path = os.path.join(dire.image_path, src)
    return FileResponse(file_path)


@router.post("/get_fol_color")
def get_fol_color(fol_col: FolderColor):
    folder_set = read_json(os.path.join(dire.json_path, "folders.json"))[fol_col.item]
    return folder_set


@router.post("/set_fol_color")
def set_fol_color(fol_col: FolderColor):
    folder_set = read_json(os.path.join(dire.json_path, "folders.json"))
    folder_set[fol_col.item] = fol_col.color
    write_json(os.path.join(dire.json_path, "folders.json"), folder_set)
    return True


@router.post("/unzip_files")
def unzip_files(file: UploadFile = File(...)):
    try:
        with ZipFile(io.BytesIO(file.file.read()), "r") as zipf:
            zipf.extractall(dire.model_path)
    except:
        raise HTTPException(status_code=523, detail="Zip file unable to be unzipped.")
    if "settings.json" not in os.listdir(dire.model_path):
        raise HTTPException(status_code=524, detail="Settings.json missing in zip file")
    move(
        os.path.join(dire.model_path, "settings.json"),
        os.path.join(dire.json_path, "settings.json"),
    )
    return True


@router.post("/upload_settings")
def upload_settings(file: UploadFile = File(...)):
    print(file.filename)
    path = os.path.join(dire.json_path, file.filename)
    with open(path, "wb+") as f:
        copyfileobj(file.file, f)
    return True
