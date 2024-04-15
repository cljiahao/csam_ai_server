from fastapi import Depends, HTTPException
from fastapi import APIRouter
from sqlalchemy.orm import Session

from apis.utils.cache import set_cache
from db.session import get_db
from db.repository.cdc_ratio import get_ratio, create_ratio
from schemas.ratio import CreateRatio


router = APIRouter()


@router.get("/read_db")
def read_db(db: Session = Depends(get_db)):
    ratio = get_ratio(db)
    return ratio


@router.post("/add_local_db")
def add_local_db(c_ratio: CreateRatio, db: Session = Depends(get_db)):
    ratio = c_ratio.model_dump()
    directory = ratio.pop("directory")
    selected = ratio.pop("selected")
    try:
        create_ratio(ratio, db)
    except:
        raise HTTPException(
            status_code=523,
            detail=f"Failed to save data into local db and move images",
        )

    set_cache(ratio["item"], directory, selected)
