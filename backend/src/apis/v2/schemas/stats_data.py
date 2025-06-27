from pydantic import BaseModel


class ItemType(BaseModel):
    item: str


class CountResult(BaseModel):
    result: int
