import json
import pytest
from unittest.mock import MagicMock
import core.constants as core_consts
from core.exceptions import MissingSettings
from utils.osHandle.unpack import check_settings_format, zip_file_exists


@pytest.fixture
def sample_name_list() -> list[str]:
    """Sample name list for testing."""
    return ["settings.json", "test.h5", "test.txt"]


@pytest.fixture
def mock_logger(mock_func_logger: MagicMock) -> MagicMock:
    """Mock logger for testing."""
    return mock_func_logger("utils.osHandle.unpack.logger")


@pytest.fixture
def mock_json_load(
    monkeypatch: pytest.MonkeyPatch,
    sample_settings_group: dict[
        str, list[dict[str, str | dict[str, dict[str, list[int]]]]]
    ],
) -> MagicMock:
    """Mock json.load to return a sample settings group."""
    mock = MagicMock(return_value=sample_settings_group)
    monkeypatch.setattr(json, "load", mock)
    return mock


@pytest.fixture
def mock_func_validate_settings_format(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mock validate_settings_format function."""

    def _mock_func_validate_settings_format(value) -> MagicMock:
        mock = MagicMock(return_value=value)
        monkeypatch.setattr("utils.osHandle.unpack.validate_settings_format", mock)
        return mock

    return _mock_func_validate_settings_format


def test_zip_file_exists_success(sample_name_list: list[str]) -> None:
    """Test zip_file_exists with valid settings and model files."""
    zip_file_exists(sample_name_list)


def test_zip_file_exists_missing_settings(
    sample_name_list: list[str], mock_logger: MagicMock
) -> None:
    """Test zip_file_exists when settings.json is missing."""
    sample_name_list.remove("settings.json")

    with pytest.raises(FileNotFoundError) as exc_info:
        zip_file_exists(sample_name_list)

    expected_message = f"{core_consts.SETTINGS_FILENAME} not found in Zip File."
    assert str(exc_info.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)


@pytest.mark.parametrize(
    "action, value", [("add", "extra.wrong"), ("remove", "test.h5")]
)
def test_zip_file_exists_wrong_model_files(
    action: str, value: str, sample_name_list: list[str], mock_logger: MagicMock
) -> None:
    """Test zip_file_exists with invalid or missing model files."""
    if action == "add":
        sample_name_list.append(value)
    elif action == "remove":
        sample_name_list.remove(value)

    with pytest.raises(ValueError) as exc_info:
        zip_file_exists(sample_name_list)

    expected_message = "Some files in the zip file do not match requirements."
    assert str(exc_info.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)


def test_check_settings_format_success(
    mock_json_load: MagicMock,
    mock_func_validate_settings_format: MagicMock,
) -> None:
    """Test check_settings_format with valid settings."""
    mock_validate_settings_format = mock_func_validate_settings_format("")

    check_settings_format(MagicMock(), core_consts.SETTINGS_FILENAME)

    mock_json_load.assert_called_once()
    mock_validate_settings_format.assert_called_once()


def test_check_settings_format_invalid_file_name(
    mock_logger: MagicMock,
) -> None:
    """Test check_settings_format with invalid file_name."""

    file_name = "test.json"
    with pytest.raises(FileNotFoundError) as exc_info:
        check_settings_format(MagicMock(), file_name)

    expected_message = f"{file_name} must be named {core_consts.SETTINGS_FILENAME}."
    assert str(exc_info.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)


def test_check_settings_format_invalid_settings(
    sample_lot_details: dict[str, str],
    mock_logger: MagicMock,
    mock_json_load: MagicMock,
    mock_func_validate_settings_format: MagicMock,
) -> None:
    """Test check_settings_format with invalid settings."""
    std_out = "invalid"
    mock_validate_settings_format = mock_func_validate_settings_format(std_out)

    with pytest.raises(MissingSettings) as exc_info:
        check_settings_format(MagicMock(), core_consts.SETTINGS_FILENAME)

    mock_json_load.assert_called_once()
    mock_validate_settings_format.assert_called_once()
    expected_message = f"Item : {sample_lot_details['item']} {std_out}"
    assert str(exc_info.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)
