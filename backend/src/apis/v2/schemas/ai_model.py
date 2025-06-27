from pydantic import BaseModel


class ModelItemHistory(BaseModel):
    id: int
    date_install: str
    item: str
    model_name: str
