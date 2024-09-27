import cv2
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import MagicMock

from core.exceptions import ImageProcessError
from utils.osHandle.initialize import initialize, save_original


MOCK_DECODED_IMAGE = np.array([[0, 0, 0], [0, 0, 0]], dtype=np.uint8)


@pytest.fixture
def mock_path_methods(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[MagicMock, MagicMock, MagicMock]:
    """Fixture to mock Path methods."""

    mock_mkdir = MagicMock()
    mock_glob = MagicMock()
    mock_rename = MagicMock()
    mock_exists = MagicMock(return_value=True)

    monkeypatch.setattr(Path, "mkdir", mock_mkdir)
    monkeypatch.setattr(Path, "glob", mock_glob)
    monkeypatch.setattr(Path, "rename", mock_rename)
    monkeypatch.setattr(Path, "exists", mock_exists)

    return mock_mkdir, mock_glob, mock_rename, mock_exists


@pytest.fixture
def mock_save_original(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Fixture to mock save_original function."""

    mock = MagicMock(return_value=MOCK_DECODED_IMAGE)
    monkeypatch.setattr("utils.osHandle.initialize.save_original", mock)
    return mock


def test_initialize_success(
    mock_file_methods: tuple[MagicMock, MagicMock],
    mock_path_methods: tuple[MagicMock, MagicMock, MagicMock],
    mock_save_original: MagicMock,
    sample_lot_details: dict[str, str],
) -> None:
    """
    Test the initialize function.

    - Ensure that directories are created properly.
    - Ensure that save_original is called with the correct parameters.
    - Ensure that the function returns the correct values.
    """
    mock_path, mock_file = mock_file_methods
    mock_mkdir, _, _, _ = mock_path_methods

    result_image, result_plate_path, result_temp_path = initialize(
        sample_lot_details["lotNo"], sample_lot_details["item"], mock_file, mock_path
    )

    # Verify directory creation
    expected_plate_path = (
        mock_path
        / sample_lot_details["item"]
        / sample_lot_details["lotNo"]
        / Path(mock_file.filename).stem
    )
    expected_temp_path = expected_plate_path / "temp"
    mock_mkdir.assert_any_call(parents=True, exist_ok=True)

    # Verify save_original call
    mock_save_original.assert_called_once_with(mock_file, expected_plate_path)

    # Verify the return values
    assert result_image is MOCK_DECODED_IMAGE
    assert result_plate_path == expected_plate_path
    assert result_temp_path == expected_temp_path


def test_save_original_success(
    mock_file_methods: tuple[MagicMock, MagicMock],
    mock_path_methods: tuple[MagicMock, MagicMock, MagicMock],
    mock_cv2_methods: tuple[MagicMock, MagicMock, MagicMock, MagicMock],
) -> None:
    """Test successful saving of the original image."""

    mock_path, mock_file = mock_file_methods
    mock_mkdir, _, _, _ = mock_path_methods
    _, _, mock_imdecode, mock_imwrite = mock_cv2_methods

    image = save_original(mock_file, mock_path)

    # Verify that all expected operations were performed
    mock_mkdir.assert_called_with(parents=True, exist_ok=True)
    mock_imdecode.assert_called_once()
    mock_imwrite.assert_called_once_with(
        str(mock_path / "original" / mock_file.filename), image
    )


def test_save_original_existing_file(
    mock_file_methods: tuple[MagicMock, MagicMock],
    mock_path_methods: tuple[MagicMock, MagicMock, MagicMock],
    mock_cv2_methods: tuple[MagicMock, MagicMock, MagicMock, MagicMock],
) -> None:
    """Test behavior when an existing file is present."""

    mock_path, mock_file = mock_file_methods
    _, mock_glob, mock_rename, mock_exists = mock_path_methods
    _, _, _, mock_imwrite = mock_cv2_methods

    # Simulate existing files
    mock_glob.return_value = ["file_already_exists.png"]
    image = save_original(mock_file, mock_path)

    # Verify that the existing file was renamed
    mock_rename.assert_called_once()
    mock_imwrite.assert_called_once_with(
        str(mock_path / "original" / mock_file.filename), image
    )


def test_save_original_error(
    mock_file_methods: tuple[MagicMock, MagicMock],
    mock_path_methods: tuple[MagicMock, MagicMock, MagicMock],
    monkeypatch: pytest.MonkeyPatch,
):
    """Test error handling when cv2 imdecode fails."""

    mock_path, mock_file = mock_file_methods
    _, mock_glob, mock_rename, mock_exists = mock_path_methods

    # Simulate an error during imdecode
    mock_imdecode = MagicMock(side_effect=Exception("cv2 error"))
    monkeypatch.setattr(cv2, "imdecode", mock_imdecode)

    with pytest.raises(ImageProcessError) as excinfo:
        save_original(mock_file, mock_path)

    assert isinstance(excinfo.value, ImageProcessError)
    assert "Error converting file to cv2 format" in str(excinfo.value)

    # Verify that rename and imwrite were not called due to the error
    mock_rename.assert_not_called()
    mock_glob.assert_called_once()
