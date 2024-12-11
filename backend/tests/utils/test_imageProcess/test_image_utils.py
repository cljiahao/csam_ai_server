import os
import math
import pytest
import numpy as np

from utils.imageProcess.image_utils import (
    chunking,
    create_border_image,
    find_batch_no,
    get_median_area,
)


def test_create_border_image(
    sample_images: dict[str, str | np.ndarray],
    sample_settings_group: dict[
        str, list[dict[str, str | dict[str, dict[str, list[int]]]]]
    ],
) -> None:
    """Test the creation of border images."""

    base_image = sample_images["base"]
    border_image, border_gray = create_border_image(
        base_image,
        sample_settings_group["settingsGroup"][0]["settings"]["chip"]["crop"],
    )

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
def test_chunking(
    start: int, end: int | None, sample_clean_contours: list[tuple[list, float]]
) -> None:
    """Test chunking of contours into approximately equal parts."""

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
def test_get_median_area(
    start: int,
    end: int | None,
    expected_result: float,
    sample_clean_contours: list[tuple[list, float]],
) -> None:
    """Test calculation of the median area of contours"""

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
def test_find_batch_no(
    x_coord: int,
    y_coord: int,
    expected_result: int,
    sample_batch_data: list[dict[str, float | int]],
) -> None:
    """Test identification of batch number based on coordinates."""

    result = find_batch_no(x_coord, y_coord, sample_batch_data)

    assert result == expected_result
