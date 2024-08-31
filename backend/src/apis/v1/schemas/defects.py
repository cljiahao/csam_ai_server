from pydantic import BaseModel


class FolderColor(BaseModel):
    colorGroup: list[dict]
