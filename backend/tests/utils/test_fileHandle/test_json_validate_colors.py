from utils.fileHandle.json import validate_colors_hex


def test_validate_colors_hex_valid() -> None:
    """Test validate_colors_hex with valid settings."""
    sample_colors = [
        {"category": "NG", "hex": "#FFFFFF"},
        {"category": "NG", "hex": "#000000"},
    ]
    result = validate_colors_hex(sample_colors)
    assert result == sample_colors


def test_validate_colors_hex_invalid() -> None:
    """Test validate_colors_hex with valid settings."""
    sample_colors = [
        {"category": "NG", "hex": "invalid"},
        {"category": "Others", "hex": "#000000"},
    ]
    expected_results = [
        {"category": "NG", "hex": "#ffff00"},
        {"category": "Others", "hex": "#000000"},
    ]
    result = validate_colors_hex(sample_colors)
    assert result == expected_results
