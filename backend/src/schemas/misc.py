from pydantic import BaseModel
from typing import Optional


class FolderColor(BaseModel):
    item: str
    color: Optional[dict] = None
