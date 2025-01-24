import cv2
import numpy as np

from interface.image_process import MaskHandlerInterface


class MaskHandler(MaskHandlerInterface):
    """A utility class for processing masks using thresholding and morphological transformations.

    Args:
        image (np.ndarray): The input grayscale image. Must be a valid 2D numpy array.
        threshold_value (int): The threshold value for binary thresholding. Defaults to 250.

    Attributes:
        image (np.ndarray): The input grayscale image.
        binary_image (np.ndarray): The binary mask created after thresholding.
    """

    def __init__(self, image: np.ndarray, threshold_value: int = 250) -> None:
        """Initializes the MaskProcessor with a grayscale image and a threshold value."""
        self.image = image
        self.binary_image = self._apply_threshold(threshold_value)

    def _apply_threshold(self, threshold_value) -> np.ndarray:
        """Create a mask from the grayscale image using thresholding and morphological transformations."""
        _, binary_image = cv2.threshold(
            self.image, threshold_value, 255, cv2.THRESH_BINARY_INV
        )

        return binary_image

    def apply_morphology(self, erode_value: int, close_value: int) -> np.ndarray:
        """Applies erosion followed by morphological closing to the binary image."""
        eroded_image = self._erode(self.binary_image, erode_value)
        closed_image = self._close(eroded_image, close_value)
        return closed_image

    @staticmethod
    def _create_kernel(kernel_size: int) -> np.ndarray:
        """Creates a square kernel for morphological operations."""
        return np.ones((kernel_size, kernel_size), dtype=np.uint8)

    def _erode(self, image: np.ndarray, kernel_size: int) -> np.ndarray:
        """Applies erosion to the binary image."""
        return cv2.morphologyEx(
            image, cv2.MORPH_ERODE, self._create_kernel(kernel_size)
        )

    def _close(self, image: np.ndarray, kernel_size: int) -> np.ndarray:
        """Applies morphological closing to an image."""
        return cv2.morphologyEx(
            image, cv2.MORPH_CLOSE, self._create_kernel(kernel_size)
        )
