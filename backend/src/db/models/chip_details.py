from datetime import datetime as dt
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    # Relationship to ChipLotDetails
    lot_details: Mapped["LotDetails"] = relationship(
        "LotDetails", back_populates="chip_details"
    )
    # Foreign key to ChipLotDetails
    lot_details_id: Mapped[int] = mapped_column(ForeignKey("lotdetails.id"))

    def __repr__(self):
        return f"<ChipDetails(id={self.id}, file_name='{self.file_name}')>"
