import numpy as np

from constants.thresholds import ChipThreshold
from interface.image_process import BatchProcessorInterface, ChipProcessorInterface
from schemas.chips_data import DefectBatch, DefectData, ImageData
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
        defect_batch_dict (dict[str, DefectBatch]): A dictionary mapping batch numbers to defect batches.
        to_predict_list (list[ImageData]): A list of image data that need prediction.
        defect_list (list[ImageData]): A list of image data classified as defects (NG).
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
        self.defect_batch_dict: dict[str, DefectBatch] = {}
        self.to_predict_list: list[ImageData] = []
        self.defect_list: list[ImageData] = []

    def process_defects(
        self,
        file_name: str,
        image: np.ndarray,
        border_pad: int,
        contour_info: ContourInfo,
    ):
        """Processes defects by classifying chips and updating batch data."""
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

        # Find and update batch
        self._update_defect_batches(defect_data, x_center, y_center)

        # Rotate chip and classify
        rotated_image = self.chip_processor.rotate_chips(image, contour_info.rect)
        self._classify_chip(contour_info, file_name, rotated_image)

    def _update_defect_batches(
        self,
        defect_data: DefectData,
        x: float,
        y: float,
    ) -> None:
        """Associates a defect with a batch based on its coordinates"""
        batch_no = self.batch_processor.find_batch_no(x, y)
        if batch_no not in self.defect_batch_dict:
            self.defect_batch_dict[batch_no] = DefectBatch(
                batch_no=batch_no, defect_files=[defect_data]
            )
        else:
            self.defect_batch_dict[batch_no].defect_files.append(defect_data)

    def _classify_chip(
        self,
        contour_info: ContourInfo,
        file_name: str,
        rotated_image: np.ndarray,
    ) -> None:
        """Classifies the chip as a defect (NG) or a chip that requires prediction."""
        prediction_image_data = ImageData(
            file_name=file_name, rotated_image=rotated_image
        )
        if (
            contour_info.area < self.chip_threshold.lower_defect_area
            or self.chip_threshold.upper_defect_area < contour_info.area
        ):
            self.defect_list.append(prediction_image_data)
        else:
            self.to_predict_list.append(prediction_image_data)
