import pytest
from unittest.mock import MagicMock
from core.exceptions import MissingSettings
from utils.fileHandle.txt import read_model_txt


@pytest.fixture
def mock_logger(mock_func_logger: MagicMock) -> MagicMock:
    """Fixture to mock the logger."""
    return mock_func_logger("utils.fileHandle.txt.logger")


@pytest.fixture
def mock_func_read_txt(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Fixture to mock the read_txt function."""

    def _mock_func_read_txt(value: list[str]) -> MagicMock:
        mock = MagicMock(return_value=value)
        monkeypatch.setattr("utils.fileHandle.txt.read_txt", mock)
        return mock

    return _mock_func_read_txt


def test_read_model_txt_exists_success(
    sample_lot_details: dict[str, str], mock_func_read_txt: MagicMock
) -> None:
    """Test reading a valid model TXT file."""

    mock_data = ["0 G\n", "1 NG\n", "2 Others\n"]
    mock_read_txt = mock_func_read_txt(mock_data)

    result = read_model_txt(sample_lot_details["item"])

    mock_read_txt.assert_called_once()
    assert result == {"0": "G", "1": "NG", "2": "Others"}


def test_read_model_txt_exists_invalid(
    sample_lot_details: dict[str, str],
    mock_logger: MagicMock,
    mock_func_read_txt: MagicMock,
) -> None:
    """Test handling an invalid format in the model TXT file."""

    item = sample_lot_details["item"]
    mock_data = ["0\n", "1 NG\n", "2 Others\n"]
    mock_read_txt = mock_func_read_txt(mock_data)

    with pytest.raises(MissingSettings) as exc_info:
        read_model_txt(item)

    mock_read_txt.assert_called_once()
    expected_message = f"Labels File: {item}.txt has an invalid format at line: {mock_data[0].strip()}."
    assert str(exc_info.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)


def test_read_model_txt_not_exists(
    sample_lot_details: dict[str, str],
    mock_logger: MagicMock,
    mock_func_read_txt: MagicMock,
) -> None:
    """Test handling a missing model TXT file."""

    item = sample_lot_details["item"]
    mock_read_txt = mock_func_read_txt([])

    with pytest.raises(MissingSettings) as exc_info:
        read_model_txt(item)

    mock_read_txt.assert_called_once()
    expected_message = f"Labels File : {item}.txt is missing dataset keys."
    assert str(exc_info.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)
