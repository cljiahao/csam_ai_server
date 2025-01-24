from datetime import datetime as dt
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Settings(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    item: Mapped[str] = mapped_column(String, index=True)
    batch_erode: Mapped[int]
    batch_close: Mapped[int]
    chip_erode: Mapped[int]
    chip_close: Mapped[int]
    chip_crop: Mapped[int]

    def __repr__(self):
        return f"<Settings(id={self.id}, item='{self.item}')>"
