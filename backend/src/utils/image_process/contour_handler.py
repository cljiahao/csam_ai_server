import os
import cv2
import numpy as np

from core.logging import logger
from schemas.contours import ContourInfo, ContourList


class ContourHandler:
    """A utility class for processing and analyzing image contours."""

    @staticmethod
    def chunking(contours: list[ContourInfo]) -> list[list[ContourInfo]]:
        """Divide contours into chunks based on CPU core count for multiprocessing."""
        cpu_count = os.cpu_count() or 1
        chunk_size = max(1, len(contours) // cpu_count)
        chunk_contours = [
            contours[i : i + chunk_size] for i in range(0, len(contours), chunk_size)
        ]

        logger.debug(f"Chunk size: {chunk_size} based on CPU Count: {cpu_count}")

        return chunk_contours

    @staticmethod
    def get_median_area(contours: list[np.ndarray]) -> float:
        """Calculate the median area of the contours in the list."""
        if not contours:
            std_out = "No contours available to calculate median area."
            logger.error(std_out)
            raise ValueError(std_out)
        contour_areas = np.array([cv2.contourArea(contour) for contour in contours])
        average_area = np.median(contour_areas)
        logger.debug(f"Average Chip Area is {average_area}")

        return average_area

    @staticmethod
    def filter_and_build_contour_info(
        contours: list[np.ndarray],
        denoise_threshold: int = 0,
    ) -> ContourList:
        """Remove noise from mask image and return contour info."""

        clean_contours = [
            ContourInfo(
                contour=contour,
                rect=cv2.minAreaRect(contour),
                area=blob_area,
            )
            for contour in contours
            if (blob_area := cv2.contourArea(contour)) > denoise_threshold
        ]
        logger.debug(
            f"Filtered {len(clean_contours)} contours based on area threshold."
        )

        return ContourList(contours=clean_contours)
