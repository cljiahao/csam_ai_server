from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from db.base_class import Base
from core.read_json import read_config


class CAI_RATIO(Base):
    id = Column(Integer, primary_key=True, index=False)
    date = Column(DateTime, default=datetime.now)
    lot_no = Column(String, nullable=False, index=True)
    plate_no = Column(String, nullable=False, index=True)
    chip_type = Column(String, nullable=False)
    no_of_batches = Column(Integer, nullable=False)
    no_of_chips = Column(Integer, nullable=False)
    no_of_pred_ng = Column(Integer)
    ng_ratio = Column(String)
    fake_ratio = Column(String)


folders = read_config("./core/json/settings.json")["folders"]

for fol in folders:
    setattr(CAI_RATIO, f"no_of_{fol}", Column(Integer))
