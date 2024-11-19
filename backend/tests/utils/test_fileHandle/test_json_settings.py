import pytest
from unittest.mock import MagicMock

from core.exceptions import MissingSettings
from utils.fileHandle.json import (
    SETTINGS_JSON_PATH,
    get_settings_json,
    write_settings_json,
)


@pytest.fixture
def mock_logger(mock_func_logger: MagicMock) -> MagicMock:
    """Provide a mock logger for testing."""
    return mock_func_logger("utils.fileHandle.json.logger")


@pytest.fixture
def mock_func_validate_settings_format(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mock the validate_settings_format function."""

    def _mock_func_validate_settings_format(value) -> MagicMock:
        mock = MagicMock(return_value=value)
        monkeypatch.setattr("utils.fileHandle.json.validate_settings_format", mock)
        return mock

    return _mock_func_validate_settings_format


def test_get_settings_json_success(
    sample_settings_group: dict[str, dict],
    mock_func_validate_settings_format: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:
    """Test successful retrieval of settings JSON data."""

    mock_validate_settings_format = mock_func_validate_settings_format("")
    mock_item, mock_read_json, _ = mock_func_settings_json_dependencies(
        sample_settings_group
    )

    result = get_settings_json(mock_item)

    mock_read_json.assert_called_once()
    mock_validate_settings_format.assert_called_once()
    assert result == sample_settings_group["settingsGroup"][0]["settings"]


def test_get_settings_json_not_exists(
    mock_logger: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:
    """Test retrieval of settings JSON data when item does not exist."""

    mock_item, mock_read_json, _ = mock_func_settings_json_dependencies(
        {"settingsGroup": []}
    )

    with pytest.raises(MissingSettings) as exc_info:
        get_settings_json(mock_item)

    mock_read_json.assert_called_once()
    expected_message = f"Item : {mock_item} not found in settings file."
    assert str(exc_info.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)


def test_get_settings_json_invalid(
    sample_settings_group: dict[str, dict],
    mock_logger: MagicMock,
    mock_func_validate_settings_format: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:
    """Test retrieval of settings JSON data when format is invalid."""

    std_out = "has invalid values."
    mock_validate_settings_format = mock_func_validate_settings_format(std_out)
    mock_item, mock_read_json, _ = mock_func_settings_json_dependencies(
        sample_settings_group
    )

    with pytest.raises(MissingSettings) as exc_info:
        get_settings_json(mock_item)

    mock_read_json.assert_called_once()
    mock_validate_settings_format.assert_called_once()
    expected_message = f"Item : {mock_item} {std_out}"
    assert str(exc_info.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)


@pytest.mark.parametrize("default", [True, False])
def test_write_settings_json_success(
    sample_settings_group: dict[str, dict],
    mock_func_validate_settings_format: MagicMock,
    mock_func_settings_json_dependencies: callable,
    default: bool,
) -> None:
    """Test successful writing of settings JSON data with or without additional data."""

    mock_validate_settings_format = mock_func_validate_settings_format("")
    mock_item, mock_read_json, mock_write_json = mock_func_settings_json_dependencies(
        {"settingsGroup": []}
    )

    sample_settings = sample_settings_group["settingsGroup"][0]["settings"]

    if default:
        write_settings_json(mock_item)
    else:
        write_settings_json(mock_item, sample_settings)

    mock_read_json.assert_called_once()
    mock_validate_settings_format.assert_called_once()
    mock_write_json.assert_called_once_with(SETTINGS_JSON_PATH, sample_settings_group)


def test_write_settings_json_success_updated(
    sample_settings_group: dict[str, dict],
    mock_func_validate_settings_format: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:
    """Test successful writing of updated settings JSON data."""

    mock_validate_settings_format = mock_func_validate_settings_format("")
    mock_item, mock_read_json, mock_write_json = mock_func_settings_json_dependencies(
        sample_settings_group
    )

    sample_settings_group["settingsGroup"][0]["settings"]["batch"]["erode"] = [5, 5]
    sample_settings = sample_settings_group["settingsGroup"][0]["settings"]

    write_settings_json(mock_item, sample_settings)

    mock_read_json.assert_called_once()
    mock_validate_settings_format.assert_called_once()
    mock_write_json.assert_called_once_with(SETTINGS_JSON_PATH, sample_settings_group)


def test_write_settings_json_invalid(
    sample_settings_group: dict[str, dict],
    mock_logger: MagicMock,
    mock_func_validate_settings_format: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:
    """Test writing settings JSON data when format is invalid."""

    std_out = "has invalid values."
    mock_validate_settings_format = mock_func_validate_settings_format(std_out)
    mock_item, mock_read_json, _ = mock_func_settings_json_dependencies(
        sample_settings_group
    )

    with pytest.raises(MissingSettings) as exc_info:
        write_settings_json(mock_item)

    mock_read_json.assert_called_once()
    mock_validate_settings_format.assert_called_once()
    expected_message = f"Item : {mock_item} {std_out}"
    assert str(exc_info.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)
