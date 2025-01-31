from fastapi import Form, File
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from apis.CDC.main import CDC
from schemas.chips import ChipDetails
from db.session import get_db


router = APIRouter()


@router.post(
    "/upload_file", response_model=ChipDetails, response_model_exclude_none=True
)
def predict_NG_chips(
    lot_no: str = Form(...),
    item: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        chip_dict, plate_path, no_of_chips, no_of_batches = CDC(lot_no, item, file, db)
    except Exception as e:
        if "detail" in dir(e):
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        raise HTTPException(
            status_code=520, detail=f"Error while processing uploaded file"
        )

    details = {
        "directory": plate_path,
        "chips": no_of_chips,
        "batches": no_of_batches,
    }

    res = ChipDetails(chips=chip_dict, details=details)

    return res
