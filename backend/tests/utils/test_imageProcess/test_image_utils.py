import os
import math
import pytest
import numpy as np

from src.utils.imageProcess.image_utils import (
    chunking,
    create_border_image,
    find_batch_no,
    get_median_area,
)


def test_create_border_image(sample_images):
    """Test border image creation."""

    base_image = sample_images["base"]
    border_image, border_gray = create_border_image(base_image)

    np.testing.assert_array_equal(border_image, sample_images["border"])
    np.testing.assert_array_equal(border_gray, sample_images["gray"])


@pytest.mark.parametrize(
    "start, end",
    [
        (0, None),  # Example test case with all elements
        (0, 20),  # Example test case with a slice
        (15, None),  # Example test case with a different slice
    ],
)
def test_chunking(start, end, sample_clean_contours):
    """Test chunking of contours."""

    contours_subset = sample_clean_contours[start:end]
    result = chunking(contours_subset)

    cpu_count = os.cpu_count() or 1
    contour_count = len(contours_subset)
    # Calculate the expected number of chunks
    expected_result = math.ceil(contour_count / (contour_count // cpu_count))

    assert len(result) == expected_result


@pytest.mark.parametrize(
    "start, end, expected_result",
    [
        (0, None, 270.0),  # Example test case with all elements
        (0, 20, 266.5),  # Example test case with a slice
        (15, None, 271.0),  # Example test case with a different slice
    ],
)
def test_get_median_area(start, end, expected_result, sample_clean_contours):
    """Test median area calculation."""

    contours_subset = sample_clean_contours[start:end]
    result = get_median_area(contours_subset)

    assert result == expected_result


@pytest.mark.parametrize(
    "x_coord, y_coord, expected_result",
    [
        (176, 178, 1),  # Example test case 1st batch
        (586, 322, 8),  # Example test case 8th batch
        (1, 70, 0),  # Example test case stray chips
    ],
)
def test_find_batch_no(x_coord, y_coord, expected_result, sample_batch_data):
    """Test batch number identification."""

    result = find_batch_no(x_coord, y_coord, sample_batch_data)

    assert result == expected_result
