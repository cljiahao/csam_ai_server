import requests
from fastapi import Depends
from sqlalchemy.orm import Session

from apis.utils.cache import selected
from db.session import get_db
from db.models.cdc_ratio import CDC_RATIO
from db.repository.utils.file_create import create_csv
from schemas.ratio import CreateRatio


def get_db_data(db: Session):
    ratio = db.query(CDC_RATIO).first()
    print(ratio)

    return ratio


def get_ratio(lot_no: str, plate_no: str, db: Session):
    ratio = (
        db.query(CDC_RATIO)
        .filter(CDC_RATIO.lot_no == lot_no, CDC_RATIO.plate_no == plate_no)
        .first()
    )

    return ratio


def create_new_ratio(ratio: CreateRatio, db: Session = Depends(get_db)):
    ratio_dict = ratio.model_dump()

    ratio_dict.pop("no_of_pred_ng")

    directory = ratio_dict.pop("directory")
    real_ng_dict = ratio_dict.pop("real_ng_dict")
    selected(directory=directory, real_ng_dict=real_ng_dict)

    no_of_chips = ratio_dict["no_of_chips"]
    no_of_real_ng = ratio_dict.pop("no_of_real_ng")
    print(no_of_real_ng)
    others = (
        no_of_real_ng["no_of_others"] if "no_of_others" in no_of_real_ng.keys() else 0
    )
    ng_ratio = round(sum(no_of_real_ng.values()) / no_of_chips * 100, 2)
    other_ratio = round(others / no_of_chips * 100, 2)

    print(
        f"Previous Lot Number: {ratio_dict['lot_no']} \
            Real NG: {sum(no_of_real_ng.values())} NG Ratio: {ng_ratio}% \
            Others: {others} Other Ratio: {other_ratio}%"
    )

    ratio_dict.update(no_of_real_ng)

    ratio = CDC_RATIO(
        **ratio_dict, ng_ratio=str(ng_ratio), other_ratio=str(other_ratio)
    )
    try:
        db.add(ratio)
        db.commit()
        db.refresh(ratio)
        return False
    except:
        return True

    # To Send via HTTP (To REALTIMEDB)
    # file_path = create_csv(ratio, directory)
    # files = {'file': open(file_path, 'rb')}
    # resp = requests.post(settings.REALTIMEDB, files=files)
    # print(f"fileSize: {int(resp.content)}")
    # if int(resp.content) == os.stat(file_path).st_size: os.remove(file_path)
