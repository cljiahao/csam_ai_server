from uuid import UUID
from pydantic import BaseModel

from schemas.chips_data import FileDataBatch


class FileDataBatchDirectory(BaseModel):
    unique_id: UUID
    directory: str
    file_data_batches: list[FileDataBatch] = []
