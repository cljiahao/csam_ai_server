from uuid import UUID
from pydantic import BaseModel


class DotColors(BaseModel):
    uuid: UUID
    label: str
    color: str
