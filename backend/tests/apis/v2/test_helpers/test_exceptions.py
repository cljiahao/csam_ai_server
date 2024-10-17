import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status

from apis.v2.helpers.HTTPExceptions import handle_exceptions
from core.exceptions import DatabaseError, ImageProcessError, MissingSettings


def test_handle_file_not_found_exception() -> None:
    """Test that FileNotFoundError is handled as a 404 HTTPException."""
    with pytest.raises(HTTPException) as exc_info:
        handle_exceptions(FileNotFoundError("File not found"))

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "File not found"


def test_handle_missing_settings_exception() -> None:
    """Test that MissingSettings exception is handled as a 404 HTTPException."""
    with pytest.raises(HTTPException) as exc_info:
        handle_exceptions(MissingSettings("Settings missing"))

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Settings missing"


def test_handle_database_error_exception() -> None:
    """Test that DatabaseError is handled as a 422 HTTPException."""
    with pytest.raises(HTTPException) as exc_info:
        handle_exceptions(DatabaseError("Database error"))

    assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert exc_info.value.detail == "Database error"


def test_handle_image_process_error_exception() -> None:
    """Test that ImageProcessError is handled as a 422 HTTPException."""
    with pytest.raises(HTTPException) as exc_info:
        handle_exceptions(ImageProcessError("Image process error"))

    assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert exc_info.value.detail == "Image process error"


def test_handle_unexpected_exception(mock_func_logger: MagicMock) -> None:
    """Test that unexpected exceptions are handled as a 400 HTTPException and logged."""

    mock_logger = mock_func_logger("apis.v2.helpers.HTTPExceptions.logger")

    with pytest.raises(HTTPException) as exc_info:
        handle_exceptions(Exception("Unexpected error"))

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        exc_info.value.detail
        == "Bad Request: The request was invalid or cannot be served."
    )
    mock_logger.error.assert_called_once_with("Unexpected error", exc_info=True)
