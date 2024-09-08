import pytest
from unittest.mock import MagicMock

import core.constants as core_consts
from core.exceptions import MissingSettings
from utils.fileHandle.json import (
    get_all_colors_json,
    get_colors_json,
    validate_colors_hex,
    write_colors_json,
)


@pytest.fixture
def mock_logger(mock_func_logger: MagicMock) -> MagicMock:
    """Provide a mock logger for testing."""
    return mock_func_logger("utils.fileHandle.json.logger")


@pytest.fixture
def sample_color_group(
    sample_lot_details: dict[str, str | int]
) -> dict[str, str | list[dict[str, str]]]:
    """Fixture to return sample colors data."""
    return {
        "colorGroup": [
            {
                "item": sample_lot_details["item"],
                "colors": [
                    {"name": "NG", "hex": "#FFFFFF"},
                    {"name": "Others", "hex": "#000000"},
                ],
            }
        ]
    }


@pytest.fixture
def mock_validate_colors_hex(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mock the validate_colors_hex function."""

    mock_validate_colors_hex = MagicMock()
    monkeypatch.setattr(
        "utils.fileHandle.json.validate_colors_hex", mock_validate_colors_hex
    )

    return mock_validate_colors_hex


def test_get_colors_json_success(
    sample_color_group: dict[str, str | list[dict[str, str]]],
    mock_validate_colors_hex: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:

    mock_item, mock_read_data, _ = mock_func_settings_json_dependencies(
        sample_color_group
    )

    sample_colors = sample_color_group["colorGroup"][0]["colors"]

    result = get_colors_json(mock_item)

    mock_read_data.assert_called_once()
    mock_validate_colors_hex.assert_called_once_with(sample_colors)
    assert result == sample_colors


def test_get_colors_json_not_exists(
    mock_logger: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:

    mock_item, mock_read_data, _ = mock_func_settings_json_dependencies(
        {"colorGroup": []}
    )

    result = get_colors_json(mock_item)

    mock_read_data.assert_called_once()
    assert result == core_consts.DEFAULT_COLORS
    mock_logger.info.assert_called_once_with(
        f"Item : {mock_item} not found in colors file."
    )


def test_get_colors_json_invalid(
    sample_color_group: dict[str, str | list[dict[str, str]]],
    mock_validate_colors_hex: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:

    mock_validate_colors_hex.side_effect = MissingSettings(
        "Invalid HEX Code format received."
    )
    mock_item, mock_read_data, _ = mock_func_settings_json_dependencies(
        sample_color_group
    )

    with pytest.raises(MissingSettings):
        get_colors_json(mock_item)

    mock_read_data.assert_called_once()
    mock_validate_colors_hex.assert_called_once()


# TODO : To continue


def test_get_all_colors_json_success(
    sample_color_group: dict[str, str | list[dict[str, str]]],
    mock_validate_colors_hex: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:

    _, mock_read_data, _ = mock_func_settings_json_dependencies(sample_color_group)

    sample_colors = sample_color_group["colorGroup"][0]["colors"]

    result = get_all_colors_json()

    mock_read_data.assert_called_once()
    assert result == sample_colors


def test_get_all_colors_json_not_exists(
    mock_logger: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:

    _, mock_read_data, _ = mock_func_settings_json_dependencies({"colorGroup": []})

    result = get_all_colors_json()

    mock_read_data.assert_called_once()
    assert result == core_consts.DEFAULT_COLORS
    mock_logger.info.assert_called_once_with(
        f"Item : {mock_item} not found in colors file."
    )


def test_get_all_colors_json_invalid(
    sample_color_group: dict[str, str | list[dict[str, str]]],
    mock_validate_colors_hex: MagicMock,
    mock_func_settings_json_dependencies: callable,
) -> None:

    mock_validate_colors_hex.side_effect = MissingSettings(
        "Invalid HEX Code format received."
    )
    _, mock_read_data, _ = mock_func_settings_json_dependencies(sample_color_group)

    with pytest.raises(MissingSettings):
        get_all_colors_json()

    mock_read_data.assert_called_once()
    mock_validate_colors_hex.assert_called_once()
