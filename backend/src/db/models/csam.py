from datetime import datetime as dt
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class CSAM_DETAILS(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    lotNo: Mapped[str] = mapped_column(String(10), index=True)
    plate: Mapped[str] = mapped_column(String, index=True)
    item: Mapped[str]
    no_of_chips: Mapped[int] = mapped_column(default=0)
    no_of_batches: Mapped[int] = mapped_column(default=0)
    no_of_pred: Mapped[int] = mapped_column(default=0)
    no_of_real: Mapped[int] = mapped_column(default=0)
    with_ai: Mapped[int] = mapped_column(default=0)

    def __repr__(self):
        return (
            f"<CSAM_DETAILS(id={self.id}, lotNo='{self.lotNo}', plate='{self.plate}')>"
        )
