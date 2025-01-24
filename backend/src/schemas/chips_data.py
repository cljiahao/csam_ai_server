from dataclasses import dataclass

import numpy as np


@dataclass
class ImageData:
    file_name: str
    rotated_image: np.ndarray


@dataclass
class DefectData:
    file_name: str
    norm_x_center: float
    norm_y_center: float
    defect_mode: str


@dataclass
class DefectBatch:
    batch_no: str
    defect_files: list[DefectData]
