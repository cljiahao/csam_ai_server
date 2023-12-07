from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session

from db.session import get_db
from db.repository.cdc_ratio import get_db_data, create_new_ratio
from schemas.ratio import CreateRatio


router = APIRouter()


@router.post("/insert_db")
def insert_db(ratio: CreateRatio, db: Session = Depends(get_db)):
    res = create_new_ratio(ratio=ratio, db=db)
    return res


@router.get("/read_db")
def read_db(db: Session = Depends(get_db)):
    ratio = get_db_data(db=db)
    return ratio
