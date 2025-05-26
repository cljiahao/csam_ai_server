from uuid import UUID
from pydantic import BaseModel


class DotColors(BaseModel):
    uuid: UUID
    defect_label: str
    hex_color: str


class ItemDotColors(BaseModel):
    item: str
    dot_colors_list: list[DotColors]
