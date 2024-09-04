import pytest
from pathlib import Path
from unittest.mock import MagicMock
from fastapi.testclient import TestClient


@pytest.fixture
def mock_exists(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mocks the Path.exists method."""

    mock_exists = MagicMock(return_value=True)
    monkeypatch.setattr(Path, "exists", mock_exists)

    return mock_exists


@pytest.fixture
def mock_file_response_method(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mocks the FileResponse method."""

    mock_file_response = MagicMock()
    monkeypatch.setattr("apis.v1.routers.retrieve.FileResponse", mock_file_response)

    return mock_file_response


def test_get_image_success(
    test_client: TestClient,
    mock_exists: MagicMock,
    mock_file_response_method: MagicMock,
) -> None:
    """Tests successful retrieval of an image."""

    src = "success"
    response = test_client.get(f"/v1/image/{src}")

    assert response.status_code == 200
    mock_exists.assert_called_once()
    mock_file_response_method.assert_called_once()


def test_get_image_not_exists(
    test_client: TestClient, mock_logging: MagicMock, mock_exists: MagicMock
) -> None:
    """Tests retrieval of a non-existent image."""

    mock_exists.return_value = False
    mock_logger = mock_logging("apis.v1.routers.retrieve.logger")

    src = "not_exists"
    response = test_client.get(f"/v1/image/{src}")

    assert response.status_code == 404
    mock_logger.error.assert_called_once_with(f"Image file not found: {src}")


def test_get_image_exception(
    test_client: TestClient,
    mock_exists: MagicMock,
    mock_file_response_method: MagicMock,
) -> None:
    """Tests retrieval of an image with an exception."""

    mock_file_response_method.side_effect = Exception("Unexpected error")

    response = test_client.get("/v1/image/exception")

    assert response.status_code == 400
    mock_exists.assert_called_once()
