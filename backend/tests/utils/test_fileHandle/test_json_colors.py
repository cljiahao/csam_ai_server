import pytest
from unittest.mock import MagicMock

import core.constants as core_consts
from core.exceptions import MissingSettings
from utils.fileHandle.json import (
    COLORS_JSON_PATH,
    get_all_colors_json,
    get_colors_json,
    write_all_colors_json,
    write_colors_json,
)


@pytest.fixture
def mock_logger(mock_func_logger: MagicMock) -> MagicMock:
    """Provide a mock logger for testing."""
    return mock_func_logger("utils.fileHandle.json.logger")


@pytest.fixture
def mock_func_validate_colors_hex(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mock the validate_colors_hex function."""

    def validate_colors_hex_side_effect(
        colors: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        for color in colors:
            if color.get("hex") == "invalid":
                color["hex"] = "#ffff00"
        return colors

    def _mock_func_validate_colors_hex(value: str = None) -> MagicMock:
        mock = MagicMock(return_value=value)
        mock.side_effect = validate_colors_hex_side_effect
        monkeypatch.setattr("utils.fileHandle.json.validate_colors_hex", mock)
        return mock

    return _mock_func_validate_colors_hex


def test_get_colors_json_success(
    sample_color_group: dict[str, str | list[dict[str, str]]],
    mock_func_validate_colors_hex: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:
    """Test successful retrieval of colors from JSON."""

    mock_item, mock_read_json, _ = mock_func_settings_json_dependencies(
        sample_color_group
    )

    sample_colors = sample_color_group["colorGroup"][0]["colors"]
    mock_validate_colors_hex = mock_func_validate_colors_hex(sample_colors)

    result = get_colors_json(mock_item)

    mock_read_json.assert_called_once()
    mock_validate_colors_hex.assert_called_once_with(sample_colors)
    assert result == sample_colors


def test_get_colors_json_not_exists(
    mock_logger: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:
    """Test handling when colors data does not exist."""

    mock_item, mock_read_json, _ = mock_func_settings_json_dependencies(
        {"colorGroup": []}
    )

    result = get_colors_json(mock_item)

    mock_read_json.assert_called_once()
    assert result == core_consts.DEFAULT_COLORS
    mock_logger.info.assert_called_once_with(
        f"Item : {mock_item} not found in colors file."
    )


def test_write_colors_json_success(
    sample_color_group: dict[str, str | list[dict[str, str]]],
    mock_func_validate_colors_hex: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:
    """Test successful writing of colors to JSON."""

    mock_item, mock_read_json, mock_write_json = mock_func_settings_json_dependencies(
        {"colorGroup": []}
    )
    sample_color_group = {"colorGroup": sample_color_group["colorGroup"][:1]}
    sample_colors = sample_color_group["colorGroup"][0]["colors"]
    mock_validate_colors_hex = mock_func_validate_colors_hex(sample_colors)

    write_colors_json(mock_item, sample_colors)

    mock_validate_colors_hex.assert_called_once_with(sample_colors)
    mock_read_json.assert_called_once()
    mock_write_json.assert_called_once_with(COLORS_JSON_PATH, sample_color_group)


@pytest.mark.parametrize("invalid", [False, True])
def test_write_colors_json_updated(
    sample_color_group: dict[str, str | list[dict[str, str]]],
    mock_func_validate_colors_hex: MagicMock,
    mock_func_settings_json_dependencies: callable,
    invalid: bool,
) -> None:
    """Test updating colors in JSON with valid and invalid HEX values."""

    if invalid:
        sample_color_group["colorGroup"][0]["colors"][0]["hex"] = "invalid"

    mock_item, mock_read_json, mock_write_json = mock_func_settings_json_dependencies(
        sample_color_group
    )

    sample_color_group["colorGroup"][0]["colors"][0]["hex"] = (
        "#ffff00" if invalid else "#000000"
    )
    sample_colors = sample_color_group["colorGroup"][0]["colors"]
    mock_validate_colors_hex = mock_func_validate_colors_hex(sample_colors)

    write_colors_json(mock_item, sample_colors)

    mock_validate_colors_hex.assert_called_once_with(sample_colors)
    mock_read_json.assert_called_once()
    mock_write_json.assert_called_once_with(COLORS_JSON_PATH, sample_color_group)


def test_get_all_colors_json_success(
    sample_color_group: dict[str, str | list[dict[str, str]]],
    mock_func_validate_colors_hex: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:
    """Test successful retrieval of all colors from JSON."""

    _, mock_read_json, _ = mock_func_settings_json_dependencies(sample_color_group)

    sample_colors = sample_color_group["colorGroup"]
    mock_validate_colors_hex = mock_func_validate_colors_hex(sample_colors)

    result = get_all_colors_json()

    mock_read_json.assert_called_once()
    assert result == sample_colors
    assert mock_validate_colors_hex.call_count == len(sample_colors)


def test_get_all_colors_json_not_exists(
    mock_func_settings_json_dependencies: callable,
) -> None:
    """Test handling when no colors data exists in the JSON."""

    _, mock_read_json, _ = mock_func_settings_json_dependencies({"colorGroup": []})

    result = get_all_colors_json()

    mock_read_json.assert_called_once()
    assert result == []


def test_write_all_colors_json_success(
    sample_color_group: dict[str, str | list[dict[str, str]]],
    mock_func_validate_colors_hex: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:
    """Test successful writing of all colors to JSON."""

    _, _, mock_write_json = mock_func_settings_json_dependencies()

    mock_validate_colors_hex = mock_func_validate_colors_hex()

    write_all_colors_json(sample_color_group["colorGroup"])

    for item_data in sample_color_group["colorGroup"]:
        mock_validate_colors_hex.assert_any_call(item_data.get("colors", []))

    mock_write_json.assert_called_once_with(COLORS_JSON_PATH, sample_color_group)


def test_write_all_colors_json_item_not_exists(
    mock_logger: MagicMock,
) -> None:
    """Test successful writing of all colors to JSON."""

    with pytest.raises(MissingSettings) as exc_info:
        write_all_colors_json({"colorGroup": []})

    expected_message = "Item type missing in colors json file."
    assert str(exc_info.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)


def test_write_all_colors_json_invalid(
    sample_color_group: dict[str, str | list[dict[str, str]]],
    mock_func_validate_colors_hex: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:
    """Test successful writing of all colors to JSON."""

    _, _, mock_write_json = mock_func_settings_json_dependencies()

    mock_validate_colors_hex = mock_func_validate_colors_hex()

    sample_color_group["colorGroup"][0]["colors"][0]["hex"] = "invalid"

    write_all_colors_json(sample_color_group["colorGroup"])

    expected_data = sample_color_group
    expected_data["colorGroup"][0]["colors"][0]["hex"] = "#ffff00"

    for item_data in sample_color_group["colorGroup"]:
        mock_validate_colors_hex.assert_any_call(item_data.get("colors", []))

    mock_write_json.assert_called_once_with(COLORS_JSON_PATH, expected_data)
