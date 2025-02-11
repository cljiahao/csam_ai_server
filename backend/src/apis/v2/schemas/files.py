from uuid import UUID
from pydantic import BaseModel

from schemas.chips_data import DefectBatch


class DefectBatchDirectory(BaseModel):
    unique_id: UUID
    directory: str
    defect_batches: list[DefectBatch] = []
