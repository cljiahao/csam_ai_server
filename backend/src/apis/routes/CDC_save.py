from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session

from db.session import get_db
from db.repository.cdc_ratio import create_new_ratio
from schemas.ratio import CreateRatio

router = APIRouter()


@router.post("/save_images")
def save_img(ratio: CreateRatio, db: Session = Depends(get_db)):
    res = create_new_ratio(ratio=ratio, db=db)
    if res:
        alert = {
            "title": "Images Failed to Save!",
            "text": "Please Try Again",
            "icon": "error",
            "confirmButtonText": "Confirm",
        }
    alert = {
        "title": "Images Saved!",
        "text": "Confirm to continue",
        "icon": "success",
        "confirmButtonText": "Confirm",
    }

    return alert
