import cv2
import numpy as np

from constants.colors import BGRColors
from constants.thresholds import ImageThreshold


class BorderCreator:
    """A utility class for creating and managing borders around an image.

    Args:
            image (np.ndarray): The input image to add borders to.
            crop_size (int): The crop size used to calculate the border padding.

    Attributes:
        image (np.ndarray): The input image for which borders are created.
        border_pad (int): The calculated padding size for the border.
        border_image (np.ndarray): The resulting image with the border added.
    """

    def __init__(self, image: np.ndarray, crop_size: int) -> None:
        """Initializes the BorderCreator with an image and crop size."""
        self.image = image
        self.border_pad = self._calculate_border_pad(crop_size)
        self.border_image = self._create_border_image()

    def _calculate_border_pad(self, crop_size: int) -> int:
        """Calculates the padding size for the border based on the crop size."""
        return ((crop_size * 141) // 100 + 9) // 10 * 10

    def _create_border_image(self) -> np.ndarray:
        """Creates an image with a border added to the original image."""
        return cv2.copyMakeBorder(
            self.image,
            self.border_pad,  # Top
            self.border_pad,  # Bottom
            self.border_pad,  # Left
            self.border_pad,  # Right
            cv2.BORDER_CONSTANT,
            value=BGRColors.BACKGROUND,
        )

    def create_blank_image(self):
        """Creates a blank image with the same dimensions as the bordered image."""
        return np.zeros(self.border_image.shape[:2], np.uint8)

    def convert_background_white(self) -> np.ndarray:
        """Converts the background of the bordered image to white based on a threshold."""
        border_image_copy = self.border_image.copy()
        background = np.all(
            border_image_copy >= ImageThreshold.BACKGROUND_THRESHOLD, axis=-1
        )
        border_image_copy[background] = BGRColors.WHITE
        return border_image_copy

    def convert_background_white_and_grayscale(self) -> np.ndarray:
        """Converts the bordered image to grayscale."""
        border_white_bg_image = self.convert_background_white()
        return cv2.cvtColor(border_white_bg_image, cv2.COLOR_BGR2GRAY)
