from pydantic import BaseModel


class Item(BaseModel):
    item: str


class ChipInfo(BaseModel):
    no_of_chips: int
    no_of_batches: int
    no_of_real: int
    no_of_pred: int | None = None


class CountResult(BaseModel):
    result: int
