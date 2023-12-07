from typing import Optional
from pydantic import BaseModel


class CreateRatio(BaseModel):
    lot_no: str
    plate_no: str
    directory: str
    chip_type: str
    real_ng_dict: dict
    no_of_batches: int
    no_of_chips: int
    no_of_pred_ng: Optional[int] = None
    no_of_real_ng: dict


class UpdateRatio(CreateRatio):
    pass


class ShowRatio(BaseModel):
    no_of_chips: int

    class Config:  # tells pydantic to convert even non dict obj to json
        from_attributes = True
