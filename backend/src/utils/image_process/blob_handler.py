import cv2
import numpy as np

from constants.colors import BGRColors
from utils.debug import error_handler


class BlobHandler:
    """A utility class for processing blobs (regions of interest) found from contours in images."""

    @error_handler()
    @staticmethod
    def create_kernel(kernel_size: int) -> np.ndarray:
        """Creates a square kernel of ones for morphological operations.

        Args:
            kernel_size: The size (width and height) of the square kernel.

        Returns:
            A NumPy ndarray representing the square kernel with uint8 data type.
        """
        return np.ones((kernel_size, kernel_size), dtype=np.uint8)

    @error_handler()
    @staticmethod
    def crop_roi(
        image: np.ndarray, x_center: float, y_center: float, padding: int
    ) -> np.ndarray:
        """Crops a region of interest (ROI) from the given image.

        Args:
            image: The input image.
            x_center: The x-coordinate of the center of the ROI.
            y_center: The y-coordinate of the center of the ROI.
            padding: The padding around the center for the ROI.

        Returns:
            The cropped ROI.
        """
        y_min = int(max(0, y_center - padding))
        y_max = int(min(image.shape[0], y_center + padding))
        x_min = int(max(0, x_center - padding))
        x_max = int(min(image.shape[1], x_center + padding))

        return image[y_min:y_max, x_min:x_max]

    @error_handler()
    @staticmethod
    def split_blobs_with_erosion(
        crop_image: np.ndarray, image: np.ndarray
    ) -> list[np.ndarray]:
        """Applies erosion and finds contours to attempt splitting blobs.

        Args:
            crop_image: The cropped image containing the blob to split.
            image: The original input image before crop.

        Returns:
            A list of contours if found, otherwise an empty list.
        """
        for x_coords in range(1, 50):
            for y_coords in range(1, 50):
                erode_kernel = np.ones((x_coords, y_coords), np.uint8)
                eroded_image = cv2.erode(crop_image, erode_kernel)
                crop_contours, _ = cv2.findContours(
                    eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )

                if not crop_contours:
                    break
                if len(crop_contours) > 1:
                    crop_image[:] = eroded_image
                    contours, _ = cv2.findContours(
                        image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                    )
                    return contours
        return []

    @error_handler()
    @staticmethod
    def get_non_red_and_black_mask(image: np.ndarray) -> np.ndarray:
        """Creates a mask excluding red and black color ranges in the HSV color space.

        Args:
            image: The input BGR image.

        Returns:
            A binary mask where non-red and non-black pixels are white.
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
        return cv2.inRange(hsv, np.array([1, 0, 0]), np.array([254, 255, 255]))

    @error_handler()
    @staticmethod
    def draw_blob_mask_from_contours(
        image: np.ndarray, contours: np.ndarray
    ) -> np.ndarray:
        """Draws a white filled mask on a black background based on the given contours.

        Args:
            image: The input image (used for shape).
            contours: The contours to draw.

        Returns:
            A binary mask with the drawn contours filled with white.
        """
        blank_mask = np.zeros(image.shape[:2], np.uint8)
        cv2.drawContours(
            blank_mask,
            [contours],
            -1,
            BGRColors.WHITE.value,
            -1,
        )
        return blank_mask

    @error_handler()
    @staticmethod
    def extract_dark_blobs_mask(
        image: np.ndarray, bright_bg_threshold: int
    ) -> np.ndarray:
        """Extracts a binary mask of dark blobs from the grayscale image.

        Args:
            image: The input BGR image.

        Returns:
            A binary mask (uint8) where dark blobs are white.
        """
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(
            gray_image, bright_bg_threshold, 255, cv2.THRESH_BINARY_INV
        )
        erode_kernel = BlobHandler.create_kernel(3)
        return cv2.erode(binary_image, erode_kernel)
