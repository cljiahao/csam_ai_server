from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session

from apis.utils.cache import set_cache
from apis.routes.HTTPException import handle_exceptions
from db.session import get_db
from db.repository.cai_ratio import create_ratio, get_all_ratio
from schemas.ratio import CreateRatio

router = APIRouter()


@router.get("/read_db")
def read_db(db: Session = Depends(get_db)):
    try:
        ratio = get_all_ratio(db)
        return ratio
    except Exception as e:
        handle_exceptions(e)


@router.post("/add_local_db")
def add_local_db(c_ratio: CreateRatio, db: Session = Depends(get_db)):
    ratio = c_ratio.model_dump()
    directory = ratio.pop("directory")
    selected = ratio.pop("selected")
    try:
        create_ratio(ratio, db)
        set_cache(ratio["item"], directory, selected)

    except Exception as e:
        handle_exceptions(e)
