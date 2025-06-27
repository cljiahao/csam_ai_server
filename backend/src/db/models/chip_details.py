from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models.lot_details import LotDetails

from datetime import datetime as dt
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from constants.folder_names import CSAMImageFolderName
from db.base import Base


class ChipDetails(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    batch_no: Mapped[str]
    file_name: Mapped[str] = mapped_column(unique=True, index=True)
    norm_x_center: Mapped[int]
    norm_y_center: Mapped[int]
    defect_mode: Mapped[str] = mapped_column(default=CSAMImageFolderName.TEMP)

    # Relationship to LotDetails
    lot_details: Mapped[LotDetails] = relationship(
        "LotDetails", back_populates="chip_details"
    )
    # Foreign key to LotDetails
    lot_details_id: Mapped[UUID] = mapped_column(ForeignKey("lotdetails.id"))

    def __repr__(self):
        return f"<ChipDetails(id={self.id}, file_name='{self.file_name}')>"
