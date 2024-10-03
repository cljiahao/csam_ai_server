import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient


@pytest.fixture
def mock_logger(mock_func_logger: MagicMock) -> MagicMock:
    """Mock logger for testing."""
    return mock_func_logger("apis.v2.routers.files.logger")


@pytest.fixture
def mock_unzip_files(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mocks the unzip_files function."""
    mock = MagicMock()
    monkeypatch.setattr("apis.v2.routers.files.unzip_files", mock)
    return mock


def test_upload_zip_success(
    test_client: TestClient,
    mock_logger: MagicMock,
    mock_file_methods: tuple[MagicMock, MagicMock],
    mock_unzip_files: MagicMock,
) -> None:

    _, mock_file = mock_file_methods
    file_data = {
        "file": (
            mock_file.filename,
            mock_file.file.read(),
            "application/x-zip-compressed",
        )
    }

    response = test_client.post(f"/v2/upload/zip", files=file_data)

    mock_logger.info.assert_called_once_with(f"{mock_file.filename} uploaded")
    mock_unzip_files.assert_called_once()
    assert response.status_code == 200


def test_upload_zip_exception(
    test_client: TestClient,
    mock_logger: MagicMock,
    mock_file_methods: tuple[MagicMock, MagicMock],
    mock_unzip_files: MagicMock,
) -> None:

    mock_unzip_files.side_effect = Exception("Unexpected Error")

    _, mock_file = mock_file_methods
    file_data = {
        "file": (
            mock_file.filename,
            mock_file.file.read(),
            "application/x-zip-compressed",
        )
    }

    response = test_client.post(f"/v2/upload/zip", files=file_data)

    mock_logger.info.assert_called_once_with(f"{mock_file.filename} uploaded")
    mock_unzip_files.assert_called_once()
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Bad Request: The request was invalid or cannot be served."
    }


def test_upload_zip_invalid(
    test_client: TestClient,
    mock_unzip_files: MagicMock,
) -> None:

    response = test_client.post(f"/v2/upload/zip", files={})

    assert response.status_code == 422
    mock_unzip_files.assert_not_called()
