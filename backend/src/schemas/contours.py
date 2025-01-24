import numpy as np
from dataclasses import dataclass
from cv2.typing import RotatedRect


@dataclass
class ContourInfo:
    contour: np.ndarray
    rect: RotatedRect
    area: float

    class Config:
        arbitrary_types_allowed = True


@dataclass
class ContourList:
    contours: list[ContourInfo]

    def __len__(self) -> int:
        return len(self.contours)

    def get_median_area(self) -> float:
        """Calculate the median area of the contours in the list."""
        if not self.contours:
            raise ValueError("No contours available to calculate median area.")
        contour_areas = np.array([contour_info.area for contour_info in self.contours])
        average_area = np.median(contour_areas)
        print(f"Average Chip Area is {average_area}")

        return average_area
