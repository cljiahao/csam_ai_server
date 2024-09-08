import pytest
from unittest.mock import MagicMock

from core.exceptions import MissingSettings
from utils.fileHandle.json import validate_colors_hex


def test_validate_colors_hex_valid():
    """Test validate_colors_hex with valid settings."""
    sample_colors = [
        {"category": "NG", "hex": "#FFFFFF"},
        {"category": "NG", "hex": "#000000"},
    ]
    assert validate_colors_hex(sample_colors) is None


def test_validate_colors_hex_invalid(mock_logger: MagicMock):
    """Test validate_colors_hex with valid settings."""
    sample_colors = [
        {"category": "NG", "hex": "invalid"},
        {"category": "Others", "hex": "#000000"},
    ]
    with pytest.raises(MissingSettings) as exc_info:
        validate_colors_hex(sample_colors)

    expected_message = "Invalid HEX Code format received."
    assert str(exc_info.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)
