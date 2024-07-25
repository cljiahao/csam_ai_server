from typing import Optional
from pydantic import BaseModel


class Details(BaseModel):
    lot: Optional[str] = None
    plate: Optional[str] = None
    item: Optional[str] = None
    directory: str
    chips: int
    batches: int
    pred_ng: Optional[int] = None
    real_ng: Optional[dict] = None


class ChipDetails(BaseModel):
    chips: dict
    details: Details
