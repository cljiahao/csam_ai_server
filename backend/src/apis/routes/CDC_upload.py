from fastapi import Form, Depends, File
from fastapi import APIRouter, UploadFile, HTTPException
from sqlalchemy.orm import Session

from apis.CDC.main import inspect
from apis.utils.check_lot import check_lot
from db.session import get_db
from db.repository.cdc_ratio import get_ratio
from schemas.chips import ShowNG
from core.read_json import read_config

router = APIRouter()


@router.post("/upload_file", response_model=ShowNG)
def show_chips(
    file: UploadFile = File(...), lot_no: str = Form(...), db: Session = Depends(get_db)
):
    print("Received file to process, please wait...")
    # Check if lot number exists or if its for testing
    chip_type = check_lot(lot_no)
    if chip_type == None:
        raise HTTPException(
            status_code=404, detail=f"Lot number: {lot_no} not found in database"
        )
    try:
        no_of_batches, no_of_chips, chips_dict, save_dir, img_shape = inspect(
            file, lot_no, chip_type, db, get_ratio
        )
    except:
        raise HTTPException(
            status_code=400, detail=f"Error while processing uploaded file"
        )

    settings = read_config("./core/json/settings.json")["folders"]

    res = ShowNG(
        plate_no=file.filename.split(".")[0],
        chips=chips_dict,
        img_shape=img_shape,
        no_of_chips=no_of_chips,
        no_of_batches=no_of_batches,
        directory=save_dir,
        chip_type=chip_type,
        settings=settings,
    )

    return res
