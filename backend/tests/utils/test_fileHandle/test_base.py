import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock

from utils.fileHandle.base import read_json, write_json, read_txt, write_txt


def test_read_json_exists():
    """Test reading an existing JSON file."""
    file_path = "test.json"
    mock_file = MagicMock()
    mock_file.read.return_value = json.dumps({"key": "value"})

    with MagicMock() as mock_open:
        mock_open.return_value = mock_file
        with open(file_path, "r") as f:
            result = read_json(file_path)
        assert result == {"key": "value"}
        mock_open.assert_called_once_with(file_path, "r")


def test_read_json_not_exists():
    """Test reading a non-existing JSON file."""
    file_path = "test_nonexistent.json"
    mock_open = MagicMock()

    # Mock the `open` function to simulate file not existing
    with MagicMock() as mock_open:
        mock_open.side_effect = FileNotFoundError
        with MagicMock() as mock_write:
            write_json_func = MagicMock()
            write_json_func.side_effect = write_json
            with open(file_path, "r") as f:
                result = read_json(file_path)
                assert result == {}
                mock_write.assert_called_once_with(file_path, {})
                mock_open.assert_called_once_with(file_path, "r")


def test_write_json():
    """Test writing to a JSON file."""
    file_path = "test_write.json"
    data = {"key": "value"}

    mock_open = MagicMock()
    mock_open.return_value = MagicMock()

    with MagicMock() as mock_open:
        with open(file_path, "w") as f:
            write_json(file_path, data)
            f.write.assert_called_once_with(json.dumps(data, indent=4))


def test_read_txt_exists():
    """Test reading an existing text file."""
    file_path = "test.txt"
    mock_file = MagicMock()
    mock_file.readlines.return_value = ["line1\n", "line2"]

    with MagicMock() as mock_open:
        mock_open.return_value = mock_file
        with open(file_path, "r") as f:
            result = read_txt(file_path)
        assert result == ["line1\n", "line2"]
        mock_open.assert_called_once_with(file_path, "r")


def test_read_txt_not_exists():
    """Test reading a non-existing text file."""
    file_path = "test_nonexistent.txt"
    mock_open = MagicMock()

    # Mock the `open` function to simulate file not existing
    with MagicMock() as mock_open:
        mock_open.side_effect = FileNotFoundError
        with MagicMock() as mock_write:
            write_txt_func = MagicMock()
            write_txt_func.side_effect = write_txt
            with open(file_path, "r") as f:
                result = read_txt(file_path)
                assert result == []
                mock_write.assert_called_once_with(file_path, [])
                mock_open.assert_called_once_with(file_path, "r")


def test_write_txt():
    """Test writing to a text file."""
    file_path = "test_write.txt"
    data = "line1\nline2"

    mock_open = MagicMock()
    mock_open.return_value = MagicMock()

    with MagicMock() as mock_open:
        with open(file_path, "w") as f:
            write_txt(file_path, data)
            f.write.assert_called_once_with(data)
