from datetime import datetime as dt
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class ImageSettings(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    item: Mapped[str] = mapped_column(String, index=True)
    batch_erode: Mapped[int] = mapped_column(default=0)
    batch_close: Mapped[int] = mapped_column(default=0)
    chip_noise_erode: Mapped[int] = mapped_column(default=0)
    chip_dilate: Mapped[int] = mapped_column(default=0)
    chip_erode: Mapped[int] = mapped_column(default=0)
    crop_size: Mapped[int] = mapped_column(default=0)

    def __repr__(self):
        return f"<Settings(id={self.id}, item='{self.item}')>"
