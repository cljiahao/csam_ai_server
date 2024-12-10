from utils.fileHandle.json import (
    validate_settings_format,
)


def test_check_settings_format_valid() -> None:
    """Test check_settings_format with valid settings."""
    sample_settings = {
        "batch": {"erode": [1, 1], "close": [1, 1]},
        "chip": {"erode": [1, 1], "close": [1, 1], "crop": [54, 54]},
    }
    assert validate_settings_format(sample_settings) is None


def test_check_settings_format_missing_key():
    """Test check_settings_format with missing key."""

    sample_settings = {"batch": {"erode": [1, 1], "close": [1, 1]}}

    assert validate_settings_format(sample_settings) == "missing key: chip."


def test_check_settings_format_missing_sub_key() -> None:
    """Test check_settings_format with missing sub key."""
    sample_settings = {
        "batch": {"erode": [1, 1]},
        "chip": {"erode": [1, 1], "close": [1, 1], "crop": [54, 54]},
    }
    assert (
        validate_settings_format(sample_settings)
        == "missing sub-keys: close in key: batch."
    )


def test_check_settings_format_invalid_list():
    """Test check_settings_format with invalid list format."""
    sample_settings = {
        "batch": {"erode": [1, 1], "close": (1, "invalid")},
        "chip": {"erode": [1, 1], "close": [1, 1], "crop": [54, 54]},
    }
    assert (
        validate_settings_format(sample_settings)
        == "have invalid lists for keys: close in key: batch."
    )
