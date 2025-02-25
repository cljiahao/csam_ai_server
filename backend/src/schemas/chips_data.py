from dataclasses import dataclass

import numpy as np


@dataclass
class ImageData:
    file_name: str
    rotated_image: np.ndarray
    to_predict: bool


@dataclass
class CoordsData:
    norm_x_center: float
    norm_y_center: float


@dataclass
class DefectData(CoordsData):
    file_name: str
    defect_mode: str


@dataclass
class BatchDefectData:
    batch_no: str
    defect_data: DefectData


@dataclass
class FileDataBatch:
    batch_no: str
    data_files: list[DefectData]
