import random
import pytest
from pathlib import Path
from unittest.mock import MagicMock

from utils.imageCache.cache import get_cache_data, set_cache_data


sample_colors = [
    {"category": "NG", "hex": "#ffff00"},
    {"category": "Others", "hex": "#00ffff"},
    {"category": "Default", "hex": "#37ff00"},
    {"category": "Default2", "hex": "#0400ff"},
]


@pytest.fixture
def mock_path_methods(monkeypatch: pytest.MonkeyPatch):
    """Fixture to mock Path methods."""

    mock_iterdir = MagicMock()
    mock_mkdir = MagicMock()
    mock_move = MagicMock()

    monkeypatch.setattr(Path, "iterdir", mock_iterdir)
    monkeypatch.setattr(Path, "mkdir", mock_mkdir)
    monkeypatch.setattr("utils.imageCache.cache.move", mock_move)

    return mock_iterdir, mock_mkdir, mock_move


@pytest.fixture
def mock_sample_files(sample_file_names: list[str]):
    """Fixture to mock Files methods"""

    sample_files = []
    for file_name in sample_file_names:
        mock_file = MagicMock()
        mock_file.name = file_name
        sample_files.append(mock_file)

    random.shuffle(sample_file_names)
    sample_selected = {
        "NG": sample_file_names[:2],
        "Others": sample_file_names[2:5],
    }

    stray_exists = any(file.name.split("_")[1] == "0" for file in sample_files)

    return sample_files, sample_selected, stray_exists


@pytest.fixture
def mock_get_colors_json(monkeypatch: pytest.MonkeyPatch):
    """Fixture to mock the get_colors_json function."""

    mock_colors = MagicMock(return_value=sample_colors)
    monkeypatch.setattr("utils.imageCache.cache.get_colors_json", mock_colors)

    return mock_colors


def test_get_cache_data(
    sample_lot_details: dict[str, str | int],
    mock_file_methods: tuple[MagicMock, MagicMock],
    mock_path_methods: tuple[MagicMock, MagicMock, MagicMock],
    mock_sample_files: tuple[list[MagicMock], dict[str, list[str]], bool],
):
    """Test the get_cache_data function."""

    mock_path, _ = mock_file_methods
    mock_iterdir, _, _ = mock_path_methods
    mock_files, _, stray_exists = mock_sample_files

    mock_folder = MagicMock()
    mock_folder.iterdir.return_value = mock_files
    mock_iterdir.return_value = [mock_folder]

    result_chip_dict = get_cache_data(sample_lot_details["no_of_batches"], mock_path)

    expected_no_of_batches = (
        sample_lot_details["no_of_batches"] + 1
        if stray_exists
        else sample_lot_details["no_of_batches"]
    )

    assert len(result_chip_dict) == expected_no_of_batches
    assert len(sum(result_chip_dict.values(), [])) == len(mock_files)


def test_set_cache_data(
    sample_lot_details: dict[str, str | int],
    mock_path_methods: tuple[MagicMock, MagicMock, MagicMock],
    mock_sample_files: tuple[list[MagicMock], dict[str, list[str]], bool],
    mock_get_colors_json: MagicMock,
):
    """Test the set_cache_data function."""
    mock_iterdir, _, mock_move = mock_path_methods
    mock_files, mock_selected, _ = mock_sample_files

    mock_folder = MagicMock()
    mock_folder.iterdir.return_value = mock_files
    mock_folder.name = "temp"
    mock_iterdir.return_value = [mock_folder]

    result = set_cache_data(sample_lot_details["item"], "relative/path", mock_selected)

    assert result is True
    mock_get_colors_json.assert_called_once_with(sample_lot_details["item"])
    assert mock_move.call_count == sum(len(value) for value in mock_selected.values())


# TODO: Test set_cache_data when some files move back to temp
