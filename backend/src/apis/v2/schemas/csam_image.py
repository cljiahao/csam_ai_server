import numpy as np
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class Coordinates(BaseModel):
    norm_x_center: float
    norm_y_center: float


class LabeledImageData(Coordinates):
    batch_no: str
    file_name: str
    image_data: np.ndarray

    model_config = ConfigDict(arbitrary_types_allowed=True)


class DefectData(Coordinates):
    file_name: str
    defect_mode: str


class FileDataBatch(BaseModel):
    batch_no: str
    defect_records: list[DefectData]


class FileDataBatchDirectory(BaseModel):
    unique_id: UUID
    directory: str
    file_data_batches: list[FileDataBatch] = []
