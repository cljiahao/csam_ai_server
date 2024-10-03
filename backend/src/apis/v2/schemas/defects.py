from pydantic import BaseModel


class CategoryHex(BaseModel):
    category: str
    hex: str


class Colors(BaseModel):
    colors: list[CategoryHex]


class ItemColors(Colors):
    item: str


class ColorGroup(BaseModel):
    colorGroup: list[ItemColors]
