import pytest
from unittest.mock import patch, mock_open
from core.exceptions import MissingSettings
from core.logging import logger
from core.directory import directory
import core.constants as core_consts

from utils.fileHandle.json import (
    check_settings_format,
    get_settings_json,
    write_settings_json,
    get_colors_json,
    write_colors_json,
)


@pytest.fixture
def mock_default_settings():
    """Fixture to return default settings."""
    return {
        "batch": {"erode": (1, 1), "close": (1, 1)},
        "chip": {"erode": (1, 1), "close": (1, 1)},
    }


@pytest.fixture
def mock_colors_data():
    """Fixture to return sample colors data."""
    return [
        {
            "item": "item1",
            "colors": [{"name": "color1", "hex": "#FFFFFF"}]
        },
        {
            "item": "item2",
            "colors": [{"name": "color2", "hex": "#000000"}]
        },
    ]


def test_check_settings_format_valid(mock_default_settings):
    """Test check_settings_format with valid settings."""
    assert check_settings_format(mock_default_settings) is None


def test_check_settings_format_missing_key():
    """Test check_settings_format with missing key."""
    settings = {"batch": {"erode": (1, 1)}}
    assert check_settings_format(settings) == "missing key: chip."


def test_check_settings_format_invalid_tuple():
    """Test check_settings_format with invalid tuple format."""
    settings = {"batch": {"erode": (1, 1), "close": (1, "invalid")}, "chip": {"erode": (1, 1), "close": (1, 1)}}
    assert check_settings_format(settings) == "have invalid tuples for keys: close in key: batch."


@patch("your_module.read_json")
def test_get_settings_json_valid(mock_read_json, mock_default_settings):
    """Test get_settings_json with valid data."""
    mock_read_json.return_value = {
        "processSettings": [{"item": "item1", "settings": mock_default_settings}]
    }
    result = get_settings_json("item1")
    assert result == mock_default_settings


@patch("your_module.read_json")
def test_get_settings_json_missing_item(mock_read_json):
    """Test get_settings_json with a missing item."""
    mock_read_json.return_value = {
        "processSettings": [{"item": "item2", "settings": {}}]
    }
    with pytest.raises(MissingSettings):
        get_settings_json("item1")


@patch("your_module.write_json")
@patch("your_module.read_json")
def test_write_settings_json(mock_read_json, mock_write_json, mock_default_settings):
    """Test write_settings_json with valid data."""
    mock_read_json.return_value = {
        "processSettings": [{"item": "item1", "settings": mock_default_settings}]
    }
    write_settings_json("item1", mock_default_settings)
    mock_write_json.assert_called_once()


@patch("your_module.read_json")
def test_get_colors_json_valid(mock_read_json, mock_colors_data):
    """Test get_colors_json with valid data."""
    mock_read_json.return_value = {"colorGroup": mock_colors_data}
    result = get_colors_json("item1")
    assert result == [{"name": "color1", "hex": "#FFFFFF"}]


@patch("your_module.read_json")
def test_get_colors_json_no_item(mock_read_json, mock_colors_data):
    """Test get_colors_json without specifying an item."""
    mock_read_json.return_value = {"colorGroup": mock_colors_data}
    result = get_colors_json()
    assert result == mock_colors_data


@patch("your_module.write_json")
@patch("your_module.read_json")
def test_write_colors_json_valid(mock_read_json, mock_write_json, mock_colors_data):
    """Test write_colors_json with valid color data."""
    mock_read_json.return_value = {"colorGroup": mock_colors_data}
    write_colors_json([{"item": "item1", "colors": [{"name": "color1", "hex": "#FFFFFF"}]}])
    mock_write_json.assert_called_once()


@patch("your_module.logger.error")
def test_write_colors_json_invalid_hex(mock_logger_error):
    """Test write_colors_json with invalid hex code."""
    with pytest.raises(MissingSettings):
        write_colors_json([{"item": "item1", "colors": [{"name": "color1", "hex": "invalid"}]}])
    mock_logger_error.assert_called_once_with("Invalid HEX Code format received.")
