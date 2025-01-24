import numpy as np
from PIL import Image
from cv2.typing import RotatedRect

from interface.image_process import ChipProcessorInterface, MaskHandlerInterface
from utils.image_process.blob_handler import BlobHandler


class ChipProcessor(ChipProcessorInterface):
    """A utility class for processing images related to chips.

    Args:
        mask_handler (MaskHandlerInterface): The mask handler for applying morphology operations.
        chip_erode (int): The erosion size for the chip mask.
        chip_close (int): The closing size for the chip mask.
        border_pad (int): The padding to apply around the chip before cropping.
        crop_size (int): The size of the crop after rotation.

    Attributes:
        border_pad (int): The padding applied to the image border before cropping.
        crop_size (int): The size to which the chips should be cropped after rotation.
        chip_mask (np.ndarray): The processed chip mask after applying morphological operations.
    """

    def __init__(
        self,
        mask_handler: MaskHandlerInterface,
        chip_erode: int,
        chip_close: int,
        border_pad: int,
        crop_size: int,
    ) -> None:
        self.border_pad = border_pad
        self.crop_size = crop_size
        self.chip_mask = mask_handler.apply_morphology(chip_erode, chip_close)

    def rotate_chips(
        self,
        image: np.ndarray,
        rect: RotatedRect,
    ) -> np.ndarray:
        """Return rotated image cropped to specified size."""

        ((x_center, y_center), (width, height), theta) = rect
        if height < width:
            theta -= 90

        pre_crop_image = BlobHandler.crop_roi(
            image, x_center, y_center, self.border_pad
        )

        pil_image = Image.fromarray(pre_crop_image)
        rotated_image = np.asarray(pil_image.rotate(theta))

        rotated_crop_image = BlobHandler.crop_roi(
            rotated_image, self.border_pad, self.border_pad, self.crop_size // 2
        )

        return rotated_crop_image
