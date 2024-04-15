import os
from apis.utils.directory import dire
from core.read_write import write_txt
from db.models.cdc_ratio import CDC_RATIO


def get_all_ratio(db):
    ratio = db.query(CDC_RATIO).first()
    print(ratio)

    return ratio


def get_ratio(lot, plate, db):
    ratio = (
        db.query(CDC_RATIO)
        .filter(CDC_RATIO.lot == lot, CDC_RATIO.plate == plate)
        .first()
    )

    return ratio


def create_ratio(ratio, db):

    ratio.pop("pred_ng")

    ratio["real_ng"] = sum(ratio["real_ng"].values())
    ratio["ng_ratio"] = round(ratio["real_ng"] / ratio["chips"] * 100, 2)

    print(
        f"Previous Lot Number: {ratio['lot']} Real NG: {ratio['real_ng']} NG Ratio: {ratio['ng_ratio']}%"
    )

    db_ratio = CDC_RATIO(**ratio)
    db.add(db_ratio)
    db.commit()
    db.refresh(db_ratio)

    f_dir = os.path.join(dire.data_send_path, "CDC")
    if not os.path.exists(f_dir):
        os.makedirs(f_dir)
    write_txt(os.path.join(f_dir, f"{ratio['lot']}.txt"), ratio)
