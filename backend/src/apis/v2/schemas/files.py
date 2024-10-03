from pydantic import BaseModel


class ChipData(BaseModel):
    chips: dict[str, list]
    directory: str
