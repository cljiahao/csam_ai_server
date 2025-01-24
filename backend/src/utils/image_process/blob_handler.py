import cv2
import numpy as np


class BlobHandler:
    """A utility class for blob found from contours of images."""

    @staticmethod
    def crop_roi(
        image: np.ndarray, x_center: float, y_center: float, padding: int
    ) -> np.ndarray:
        """Crops a region of interest (ROI) from the given image based on a rotated rectangle."""
        # Ensure the crop does not go out of image bounds
        y_min = int(max(0, y_center - padding))
        y_max = int(min(image.shape[0], y_center + padding))
        x_min = int(max(0, x_center - padding))
        x_max = int(min(image.shape[1], x_center + padding))

        return image[y_min:y_max, x_min:x_max]

    @staticmethod
    def erode_and_find_contours(
        image: np.ndarray, max_kernel_size: int = 15
    ) -> list[np.ndarray]:
        """Applies erosion on the image with varying kernel sizes to attempt splitting contours."""
        for x_coords in range(1, max_kernel_size + 1):
            for y_coords in range(1, max_kernel_size + 1):
                erode_kernel = np.ones((x_coords, y_coords), np.uint8)
                image[:] = cv2.erode(image, erode_kernel)
                new_contours, _ = cv2.findContours(
                    image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )

                if not new_contours:
                    break
                if len(new_contours) > 1:
                    return new_contours
        return []
