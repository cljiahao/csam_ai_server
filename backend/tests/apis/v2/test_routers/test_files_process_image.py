import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from apis.v2.schemas.base import Module


@pytest.fixture
def sample_res_dict() -> dict[str, str | dict[str, list[str]]]:
    """Returns a sample response dictionary for image processing."""
    return {
        "chips": {
            "1": ["test.png", "test.png"],
            "2": ["test.png", "test.png"],
        },
        "directory": "./path",
    }


@pytest.fixture
def mock_process_n_predict(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mocks the process_n_predict function."""
    mock = MagicMock()
    monkeypatch.setattr("apis.v2.routers.files.process_n_predict", mock)
    return mock


@pytest.mark.parametrize("mock_module", [Module.cai.value, Module.cdc.value])
def test_process_image_success(
    test_client: TestClient,
    mock_module: str,
    sample_lot_details: dict[str, str],
    sample_res_dict: dict[str, str | dict[str, list[str]]],
    mock_file_methods: tuple[MagicMock, MagicMock],
    mock_process_n_predict: MagicMock,
) -> None:
    """Tests image processing success scenarios."""
    mock_lot_no = sample_lot_details["lotNo"]
    mock_item = sample_lot_details["item"]

    _, mock_file = mock_file_methods
    file_data = {"file": (mock_file.filename, mock_file.file.read(), "image/png")}

    mock_process_n_predict.return_value = sample_res_dict

    response = test_client.post(
        f"/v2/upload/image/{mock_module}/{mock_lot_no}/{mock_item}", files=file_data
    )

    mock_process_n_predict.assert_called_once()
    assert response.status_code == 200
    assert response.json() == sample_res_dict


def test_process_image_exception(
    test_client: TestClient,
    sample_lot_details: dict[str, str],
    mock_file_methods: tuple[MagicMock, MagicMock],
    mock_process_n_predict: MagicMock,
) -> None:
    """Tests handling of exceptions during image processing."""
    mock_module = Module.cdc.value
    mock_lot_no = sample_lot_details["lotNo"]
    mock_item = sample_lot_details["item"]

    mock_process_n_predict.side_effect = Exception("Unexpected Error")

    _, mock_file = mock_file_methods
    file_data = {"file": (mock_file.filename, mock_file.file.read(), "image/png")}

    response = test_client.post(
        f"/v2/upload/image/{mock_module}/{mock_lot_no}/{mock_item}", files=file_data
    )

    mock_process_n_predict.assert_called_once()
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Bad Request: The request was invalid or cannot be served."
    }


@pytest.fixture
def sample_invalid_args(
    request: pytest.FixtureRequest, sample_lot_details: dict[str, str]
) -> tuple[str, str, str, dict[str, tuple]]:
    """Provides sample arguments for invalid image processing."""
    lot_no = sample_lot_details["lotNo"]
    item = sample_lot_details["item"]
    file_data = {"file": ()}

    return [
        ("invalid_module", lot_no, item, file_data),
        (Module.cdc.value, "invalid_lot_no", item, file_data),
        (Module.cai.value, lot_no, item, {}),
    ][request.param]


@pytest.mark.parametrize("sample_invalid_args", [0, 1], indirect=True)
def test_process_image_invalid(
    test_client: TestClient,
    sample_invalid_args: tuple[str, str, str, dict[str, tuple]],
    mock_file_methods: tuple[MagicMock, MagicMock],
    mock_process_n_predict: MagicMock,
) -> None:
    """Tests image processing with invalid arguments."""
    mock_module, mock_lot_no, mock_item, mock_file_data = sample_invalid_args

    _, mock_file = mock_file_methods
    if mock_file_data:
        mock_file_data["file"] = (
            mock_file.filename,
            mock_file.file.read(),
            "image/png",
        )

    response = test_client.post(
        f"/v2/upload/image/{mock_module}/{mock_lot_no}/{mock_item}",
        files=mock_file_data,
    )

    assert response.status_code == 422
    mock_process_n_predict.assert_not_called()
