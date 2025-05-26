import cv2
import os
import numpy as np

from core.logging import logger
from schemas.contours import ContourInfo, ContourInfoList
from schemas.misc import NormalizeCoordinates
from utils.debug import error_handler
from utils.misc.calculations import normalize_coordinates


class ContourHandler:
    """A utility class for processing and analyzing image contours."""

    @error_handler()
    @staticmethod
    def chunking(contours: list[ContourInfo]) -> list[list[ContourInfo]]:
        """Divide contours into chunks based on CPU core count for multiprocessing.

        Args:
            contours: A list of ContourInfo objects.

        Returns:
            A list of lists of ContourInfo objects, representing chunks.
        """
        cpu_count = os.cpu_count() or 1
        chunk_size = max(1, len(contours) // cpu_count)
        chunk_contours = [
            contours[i : i + chunk_size] for i in range(0, len(contours), chunk_size)
        ]
        logger.debug(f"Chunk size: {chunk_size} based on CPU Count: {cpu_count}")

        return chunk_contours

    @error_handler()
    @staticmethod
    def get_median_area(contours: list[np.ndarray]) -> float:
        """Calculate the median area of the contours in the list.

        Args:
            contours: A list of NumPy arrays representing contours.

        Returns:
            The median area of the contours.

        Raises:
            ValueError: If the input list is empty.
        """
        if not contours:
            raise ValueError("No contours available to calculate median area.")
        contour_areas = np.array([cv2.contourArea(contour) for contour in contours])
        average_area = np.median(contour_areas)
        logger.debug(f"Average Chip Area is {average_area}")

        return average_area

    @error_handler()
    @staticmethod
    def filter_and_build_contour_info(
        contours: list[np.ndarray],
        denoise_threshold: int = 0,
    ) -> ContourInfoList:
        """Filters contours based on area and builds a ContourInfoList.

        Args:
            contours: A list of NumPy arrays representing contours.
            denoise_threshold: The minimum area for a contour to be included.

        Returns:
            A ContourInfoList object containing filtered ContourInfo objects.
        """
        clean_contours = [
            ContourInfo(
                contour=contour,
                rect=cv2.minAreaRect(contour),
                area=blob_area,
            )
            for contour in contours
            if (blob_area := cv2.contourArea(contour)) > denoise_threshold
        ]

        processed_contours = []
        for contour_info in clean_contours:
            center, (width, height), angle = contour_info.rect
            if width > height:
                contour_info.rect = (center, (height, width), angle)
            processed_contours.append(contour_info)

        logger.debug(
            f"Filtered {len(clean_contours)} contours based on area threshold.",
            stacklevel=2,
        )

        return ContourInfoList(contours=processed_contours)

    @error_handler()
    @staticmethod
    def extract_norm_coordinates(
        contour_info_list: ContourInfoList,
        image_size: tuple[int, int],
        rect_index: int = 0,
    ) -> list[NormalizeCoordinates]:
        """Extracts and normalizes coordinates from a specified rectangle within each contour.

        Args:
            contour_info_list: A ContourInfoList object containing contour information.
            image_size: A tuple containing the (height, width) of the image.
            rect_index: The index of the rectangle within the contour's 'rect' list
                        to extract coordinates from (default: 0).

        Returns:
            A list of NormalizeCoordinates objects representing the normalized
            coordinates extracted from the specified rectangle of each contour.
        """
        return [
            normalize_coordinates(contour_info.rect[rect_index], image_size)
            for contour_info in contour_info_list
        ]
