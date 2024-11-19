import cv2
import pytest
from unittest.mock import MagicMock

from utils.osHandle.write_image import (
    write_image,
    update_chip_dict,
)


@pytest.mark.parametrize("ai", [False, True])
def test_write_image(
    mock_file_methods: tuple[MagicMock, MagicMock],
    mock_cv2_methods: tuple[MagicMock, MagicMock, MagicMock, MagicMock],
    ai: bool,
) -> None:
    """Test the write_image function with mocked cv2 methods."""

    mock_path, mock_file = mock_file_methods
    mock_image, mock_cvtColor, _, mock_imwrite = mock_cv2_methods
    chip_dict = {}

    write_image(chip_dict, mock_path, mock_file.filename, mock_image, ai)

    if ai:
        mock_cvtColor.assert_called_once_with(mock_image, cv2.COLOR_RGB2BGR)
    else:
        mock_cvtColor.assert_not_called()
    mock_imwrite.assert_called_once_with(
        str(mock_path / mock_file.filename), mock_image
    )


@pytest.mark.parametrize(
    "file_name, expected_batch",
    [("batch_1_100_image.png", "1"), ("batch_0_100_image.png", "Stray")],
)
def test_update_chip_dict(file_name: str, expected_batch: str) -> None:
    """Test the update_chip_dict function."""

    chip_dict = {}

    update_chip_dict(chip_dict, file_name)

    # Verify dictionary update
    assert expected_batch in chip_dict
    assert file_name in chip_dict[expected_batch]
