from fastapi import Form, File
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from apis.CAI.main import CAI
from schemas.chips import ChipDetails
from db.session import get_db


router = APIRouter()


@router.post(
    "/upload_file", response_model=ChipDetails, response_model_exclude_none=True
)
def predict_NG_chips(
    lot_no: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)
):
    try:
        chip_dict, item, plate_path, no_of_chips, no_of_batches = CAI(lot_no, file, db)
    except Exception as e:
        if "detail" in dir(e):
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        raise HTTPException(
            status_code=520, detail=f"Error while processing uploaded file"
        )

    no_of_pred = sum(
        [len(chip_dict[x]) for x in chip_dict if isinstance(chip_dict[x], list)]
    )

    details = {
        "item": item,
        "directory": plate_path,
        "chips": no_of_chips,
        "batches": no_of_batches,
        "pred_ng": no_of_pred,
    }

    res = ChipDetails(chips=chip_dict, details=details)

    return res
