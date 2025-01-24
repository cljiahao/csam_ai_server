import cv2

from interface.image_process import BatchProcessorInterface, MaskHandlerInterface
from constants.thresholds import ImageThreshold
from core.logging import logger
from schemas.contours import ContourList
from utils.image_process.contour_handler import ContourHandler


class BatchProcessor(BatchProcessorInterface):
    """A utility class for processing images related to batch.

    Args:
        mask_handler (MaskHandlerInterface): The mask handler for morphological operations.
        batch_erode (int): The erosion size for the batch mask.
        batch_close (int): The closing size for the batch mask.

    Attributes:
        batch_mask (np.ndarray): The processed mask image used for contour extraction.
        batch_data (list): A list of dictionaries containing batch information,
                           each having 'index', 'x1', 'y1', 'x2', and 'y2'.
    """

    def __init__(
        self,
        mask_handler: MaskHandlerInterface,
        batch_erode: int,
        batch_close: int,
    ) -> None:
        self.batch_mask = mask_handler.apply_morphology(batch_erode, batch_close)

    def get_batch_data(self):
        """Returns sorted batch data based on contours."""
        contours, _ = cv2.findContours(
            self.batch_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        contour_info_list = ContourHandler.filter_and_build_contour_info(contours)

        batch_data = self._get_batch_data_from_contour_info(contour_info_list)
        self.batch_data = batch_data

        logger.debug("Number of Batches found: %s", len(batch_data))
        return batch_data

    def _get_batch_data_from_contour_info(self, contour_info_list: ContourList) -> list:
        """Generates batch data from contour information."""
        batch_data = []
        threshold_area = self._calculate_threshold_area()
        factor = self._calculate_factor()

        for contour_info in contour_info_list.contours:
            if contour_info.area < threshold_area:
                continue
            x, y, w, h = cv2.boundingRect(contour_info.contour)
            xc, yc = x + w / 2, y + h / 2
            index = round(yc / factor, 1) * factor**2 + xc

            batch_data.append(
                {"index": index, "x1": x, "y1": y, "x2": x + w, "y2": y + h}
            )

        return sorted(batch_data, key=lambda x: x["index"])

    def _calculate_threshold_area(self) -> int:
        """Calculates the threshold area based on image dimensions."""
        image_height, image_width = self.batch_mask.shape[:2]
        return image_height * image_width * ImageThreshold.BATCH_MULTIPLIER

    def _calculate_factor(self) -> int:
        """Calculates the factor used to organize batch data."""
        image_height = self.batch_mask.shape[0]
        return image_height - image_height % -1000

    def find_batch_no(self, x: float, y: float) -> str:
        """Finds the batch number for the given coordinates."""
        for i, coord in enumerate(self.batch_data):
            if self._is_within_bounds(x, y, coord):
                return str(i + 1)
        return "Stray"

    def _is_within_bounds(self, x: float, y: float, coord: dict) -> bool:
        """Checks if the given coordinates are within the bounding box."""
        return coord["x1"] <= x <= coord["x2"] and coord["y1"] <= y <= coord["y2"]
