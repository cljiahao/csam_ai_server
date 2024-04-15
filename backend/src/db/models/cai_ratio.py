from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from db.base_class import Base


class CAI_RATIO(Base):
    id = Column(Integer, primary_key=True, index=False)
    date = Column(DateTime, default=datetime.now)
    lot = Column(String, nullable=False, index=True)
    plate = Column(String, nullable=False, index=True)
    item = Column(String, nullable=False)
    chips = Column(Integer, nullable=False)
    batches = Column(Integer, nullable=False)
    pred_ng = Column(Integer)
    real_ng = Column(Integer)
    ng_ratio = Column(String)
    fake_ratio = Column(String)
