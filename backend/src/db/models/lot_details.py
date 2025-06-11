from uuid import uuid4, UUID
from datetime import datetime as dt
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class LotDetails(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    lot_no: Mapped[str] = mapped_column(String(10), index=True)
    plate_no: Mapped[str] = mapped_column(index=True)
    item: Mapped[str]
    no_of_chips: Mapped[int] = mapped_column(default=0)
    no_of_batches: Mapped[int] = mapped_column(default=0)
    no_of_pred: Mapped[int] = mapped_column(default=0)
    no_of_real: Mapped[int] = mapped_column(default=0)
    is_ai: Mapped[int] = mapped_column(default=0)

    # Relationship to ChipDetails
    chip_details: Mapped[list["ChipDetails"]] = relationship(
        "ChipDetails", back_populates="lot_details"
    )

    def __repr__(self):
        return f"<LotDetails(id={self.id}, lot_no='{self.lot_no}', plate_no='{self.plate_no}')>"
