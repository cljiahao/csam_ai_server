import cv2
import numpy as np

from constants.colors import BGRColors
from utils.debug import error_handler


class BorderCreator:
    """A utility class for creating and managing borders around an image."""

    @error_handler()
    @staticmethod
    def create_border_image(image: np.ndarray, border_padding: int = 0) -> np.ndarray:
        """Creates an image with a constant color border.

        Args:
            image: The input image.
            border_padding: The padding size for all sides of the border.

        Returns:
            The image with the added border.
        """
        return cv2.copyMakeBorder(
            image,
            border_padding,  # Top
            border_padding,  # Bottom
            border_padding,  # Left
            border_padding,  # Right
            cv2.BORDER_CONSTANT,
            value=BGRColors.BACKGROUND.value,
        )

    @error_handler()
    @staticmethod
    def convert_background_white(
        image: np.ndarray, background_threshold: int = 0
    ) -> np.ndarray:
        """Converts the background of an image to white based on a threshold.

        Assumes the background color is close to black.

        Args:
            image: The input image.
            background_threshold: The threshold value for each color channel (B, G, R)
                                  to be considered background.

        Returns:
            The image with the background pixels set to white.
        """
        border_image_copy = image.copy()
        background = np.all(border_image_copy >= background_threshold, axis=-1)
        border_image_copy[background] = BGRColors.WHITE.value
        return border_image_copy

    @error_handler()
    @staticmethod
    def convert_grayscale(image: np.ndarray) -> np.ndarray:
        """Converts a BGR image to grayscale.

        Args:
            image: The input BGR image.

        Returns:
            The grayscale image.
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @error_handler()
    @staticmethod
    def convert_background_white_and_grayscale(
        image: np.ndarray, background_threshold: int = 0
    ) -> np.ndarray:
        """Converts the background of an image to white and then converts it to grayscale.

        Args:
            image: The input BGR image.
            background_threshold: The threshold value for each color channel (B, G, R)
                                  to be considered background.

        Returns:
            np.ndarray: The grayscale image with a white background.
        """
        border_white_bg_image = BorderCreator.convert_background_white(
            image, background_threshold
        )
        return cv2.cvtColor(border_white_bg_image, cv2.COLOR_BGR2GRAY)

    @error_handler()
    @staticmethod
    def change_border_color(
        image: np.ndarray, border_width: int, border_color: tuple[int, int, int]
    ) -> np.ndarray:
        """Changes the color of the border of an image.

        Args:
            image: The input image.
            border_width: The width of the border to change.
            border_color: The BGR color to set the border to.

        Returns:
            A copy of the image with the modified border color.
        """
        image_copy = image.copy()
        image_copy[:border_width, :] = border_color
        image_copy[-border_width:, :] = border_color
        image_copy[border_width:-border_width, :border_width] = border_color
        image_copy[border_width:-border_width, -border_width:] = border_color
        return image_copy
