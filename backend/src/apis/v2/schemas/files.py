from pydantic import BaseModel

from schemas.chips_data import DefectBatch


class DefectBatchDirectory(BaseModel):
    unique_id: str
    directory: str
    defect_batches: list[DefectBatch] = []
