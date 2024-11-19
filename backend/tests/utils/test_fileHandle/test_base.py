import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, mock_open

from utils.fileHandle.base import read_json, read_txt


MOCK_JSON_FILE_PATH = "./path/test.json"
MOCK_TXT_FILE_PATH = "./path/test.txt"


@pytest.fixture
def mock_exists(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mocks the Path.exists method."""

    mock = MagicMock(return_value=True)
    monkeypatch.setattr(Path, "exists", mock)
    return mock


@pytest.fixture
def mock_func_file_open(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Fixture to mock file opening."""

    def _mock_func_file_open(read_data: str) -> MagicMock:
        mock = mock_open(read_data=read_data)
        monkeypatch.setattr("builtins.open", mock)
        return mock

    return _mock_func_file_open


def test_read_json_exists(
    mock_exists: MagicMock,
    mock_func_file_open: MagicMock,
) -> None:
    """Test reading JSON when the file exists."""

    mock_json_data = {"key": "value"}
    mock_file_open = mock_func_file_open(json.dumps(mock_json_data))

    result = read_json(MOCK_JSON_FILE_PATH)

    mock_exists.assert_called_once()
    assert result == mock_json_data
    mock_file_open.assert_called_once_with(Path(MOCK_JSON_FILE_PATH), "r")


def test_read_json_not_exists(
    mock_func_write_json: MagicMock, mock_exists: MagicMock
) -> None:
    """Test reading JSON when the file does not exist."""

    mock_exists.return_value = False

    mock_write_json = mock_func_write_json("utils.fileHandle.base.write_json")

    result = read_json(MOCK_JSON_FILE_PATH)

    mock_exists.assert_called_once()
    assert result == {}
    mock_write_json.assert_called_once_with(Path(MOCK_JSON_FILE_PATH), {})


def test_read_txt_exists(
    mock_exists: MagicMock,
    mock_func_file_open: MagicMock,
) -> None:
    """Test reading TXT when the file exists."""

    mock_txt_data = ["0 G\n", "1 NG\n", "2 Others\n"]
    mock_file_open = mock_func_file_open("".join(mock_txt_data))

    result = read_txt(MOCK_TXT_FILE_PATH)

    mock_exists.assert_called_once()
    assert set(result) == set(mock_txt_data)
    mock_file_open.assert_called_once_with(Path(MOCK_TXT_FILE_PATH), "r")


def test_read_txt_not_exists(
    monkeypatch: pytest.MonkeyPatch, mock_exists: MagicMock
) -> None:
    """Test reading TXT when the file does not exist."""

    mock_exists.return_value = False

    monkeypatch.setattr("utils.fileHandle.base.write_txt", MagicMock())

    result = read_txt(MOCK_TXT_FILE_PATH)

    mock_exists.assert_called_once()
    assert result == []
