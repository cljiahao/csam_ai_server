import os
from datetime import datetime as dt

from apis.utils.directory import dire
from core.config import settings
from core.transfer import write_csv, via_http
from db.models.cai_ratio import CAI_RATIO


def get_all_ratio(db):
    ratio = db.query(CAI_RATIO).first()
    print(ratio)

    return ratio


def get_ratio(lot, plate, db):
    ratio = (
        db.query(CAI_RATIO)
        .filter(CAI_RATIO.lot == lot, CAI_RATIO.plate == plate)
        .first()
    )

    return ratio


def create_ratio(ratio, db):

    # TODO: set individual colour to quantity
    ratio["real_ng"] = sum(ratio["real_ng"].values())
    ratio["ng_ratio"] = round(ratio["real_ng"] / ratio["chips"] * 100, 2)
    ratio["fake_ratio"] = (
        round((1 - ratio["real_ng"] / ratio["pred_ng"]) * 100, 2)
        if ratio["pred_ng"] != 0
        else 0
    )

    print(
        f"Previous Lot Number: {ratio['lot']} \
        Pred NG: {ratio['pred_ng']} Real NG: {ratio['real_ng']} \
        NG Ratio: {ratio['ng_ratio']}% FakeRatio: {ratio['fake_ratio']}%"
    )

    db_ratio = CAI_RATIO(**ratio)
    db.add(db_ratio)
    db.commit()
    db.refresh(db_ratio)

    f_dir = os.path.join(dire.data_send_path, "CAI")
    if not os.path.exists(f_dir):
        os.makedirs(f_dir)
    data = f",,,{ratio['lot']},{dt.now().strftime('%d%m%y %H%M%S')}"
    del ratio["lot"]
    csv_path = write_csv(f_dir, settings.TABLEID_CAI, data, ratio)
    via_http(csv_path)
