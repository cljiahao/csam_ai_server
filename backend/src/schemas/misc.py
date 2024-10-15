from pydantic import BaseModel
from typing import Optional


class CheckItem(BaseModel):
    lot_no: str


class FolderColor(BaseModel):
    item: str
    color: Optional[dict] = None
