from datetime import datetime as dt
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class ModelHistory(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    item: Mapped[str] = mapped_column(String, index=True, unique=True)
    ai_model_name: Mapped[str] = mapped_column(String, index=True, unique=True)
    model_label_file_name: Mapped[str] = mapped_column(String, index=True, unique=True)

    def __repr__(self):
        return f"<ModelHistory(id={self.id}, item='{self.item}')>"
