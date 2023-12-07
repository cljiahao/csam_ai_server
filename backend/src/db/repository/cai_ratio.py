import requests
from fastapi import Depends
from sqlalchemy.orm import Session

from apis.utils.cache import selected
from db.session import get_db
from db.models.cai_ratio import CAI_RATIO
from db.repository.utils.file_create import create_csv
from schemas.ratio import CreateRatio


def get_db_data(db: Session):
    ratio = db.query(CAI_RATIO).first()
    print(ratio)

    return ratio


def get_ratio(lot_no: str, plate_no: str, db: Session):
    ratio = (
        db.query(CAI_RATIO)
        .filter(CAI_RATIO.lot_no == lot_no, CAI_RATIO.plate_no == plate_no)
        .first()
    )

    return ratio


def create_new_ratio(ratio: CreateRatio, db: Session = Depends(get_db)):
    ratio_dict = ratio.model_dump()

    directory = ratio_dict.pop("directory")
    real_ng_dict = ratio_dict.pop("real_ng_dict")
    selected(directory=directory, real_ng_dict=real_ng_dict)

    no_of_chips = ratio_dict["no_of_chips"]
    no_of_pred_ng = ratio_dict["no_of_pred_ng"]
    no_of_real_ng = ratio_dict.pop("no_of_real_ng")
    ng_ratio = round(sum(no_of_real_ng.values()) / no_of_chips * 100, 2)
    fake_ratio = (
        round(sum(no_of_real_ng.values()) / no_of_pred_ng * 100, 2)
        if no_of_pred_ng != 0
        else 0
    )

    print(
        f"Previous Lot Number: {ratio_dict['lot_no']} \
            Pred NG: {no_of_pred_ng} Real NG: {sum(no_of_real_ng.values())} \
            NG Ratio: {ng_ratio}% FakeRatio: {fake_ratio}%"
    )

    ratio_dict.update(no_of_real_ng)

    ratio = CAI_RATIO(**ratio_dict, ng_ratio=str(ng_ratio), fake_ratio=str(fake_ratio))

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
