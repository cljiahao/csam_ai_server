from uuid import UUID
from datetime import datetime as dt
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class DotColors(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    item: Mapped[str] = mapped_column(index=True)
    defect_label: Mapped[str]
    hex_color: Mapped[str]
    uuid: Mapped[UUID] = mapped_column(index=True, unique=True)

    def __repr__(self):
        return f"<Colors(id={self.id}, item='{self.item}')>"
