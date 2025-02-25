import numpy as np

from constants.chip_thresholds import ChipThreshold
from interface.image_process import BatchProcessorInterface, ChipProcessorInterface
from schemas.chips_data import BatchDefectData, DefectData, ImageData
from schemas.contours import ContourInfo


class DefectProcessor:
    """A utility class for processing defects in images related to chips, including defect classification and batch processing.

    Args:
        batch_processor (BatchProcessorInterface): The batch processor interface.
        chip_processor (ChipProcessorInterface): The chip processor interface.
        chip_threshold (ChipThreshold): The thresholds for chip defect classification.

    Attributes:
        batch_processor (BatchProcessorInterface): The interface for batch processing.
        chip_processor (ChipProcessorInterface): The interface for chip processing.
        chip_threshold (ChipThreshold): The thresholds used to classify defects.
    """

    def __init__(
        self,
        batch_processor: BatchProcessorInterface,
        chip_processor: ChipProcessorInterface,
        chip_threshold: ChipThreshold,
    ):
        self.batch_processor: BatchProcessorInterface = batch_processor
        self.chip_processor: ChipProcessorInterface = chip_processor
        self.chip_threshold: ChipThreshold = chip_threshold

    def process_defects(
        self,
        file_name: str,
        image: np.ndarray,
        contour_info: ContourInfo,
        border_pad: int,
    ) -> tuple[BatchDefectData, ImageData]:
        """Processes defects by classifying chips and updating batch data."""

        batch_defect_data = self._create_defect_data(
            file_name, image, contour_info, border_pad
        )
        image_data = self._classify_chip_to_predict(file_name, image, contour_info)

        return batch_defect_data, image_data

    def _create_defect_data(
        self,
        file_name: str,
        image: np.ndarray,
        contour_info: ContourInfo,
        border_pad: int,
    ) -> BatchDefectData:
        x_center, y_center = contour_info.rect[0]
        height, width = image.shape[:2]
        norm_x_center = round((x_center - border_pad) / (width - border_pad * 2), 6)
        norm_y_center = round((y_center - border_pad) / (height - border_pad * 2), 6)

        # Create DefectData instance
        defect_data = DefectData(
            file_name=file_name,
            norm_x_center=norm_x_center,
            norm_y_center=norm_y_center,
            defect_mode="temp",
        )

        batch_no = self.batch_processor.find_batch_no(x_center, y_center)

        return BatchDefectData(batch_no=batch_no, defect_data=defect_data)

    def _classify_chip_to_predict(
        self,
        file_name: str,
        image: np.ndarray,
        contour_info: ContourInfo,
    ) -> ImageData:
        """Classifies the chip that requires prediction or not."""
        rotated_image = self.chip_processor.rotate_chips(image, contour_info.rect)

        to_predict = not (
            contour_info.area < self.chip_threshold.LOWER_DEFECT_AREA
            or self.chip_threshold.UPPER_DEFECT_AREA < contour_info.area
        )

        return ImageData(
            file_name=file_name, rotated_image=rotated_image, to_predict=to_predict
        )
