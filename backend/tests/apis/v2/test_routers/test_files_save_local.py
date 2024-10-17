import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from apis.v2.schemas.base import Module


@pytest.fixture
def sample_res_dict() -> dict[str, str | dict[str, list[str]]]:
    """Provides a sample response dictionary for image processing."""
    return {
        "chips": {
            "1": ["test.png", "test.png"],
            "2": ["test.png", "test.png"],
        },
        "directory": "./path",
    }


@pytest.fixture
def mock_set_cache_data(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mocks the set_cache_data function."""
    mock = MagicMock()
    monkeypatch.setattr("apis.v2.routers.files.set_cache_data", mock)
    return mock


# TODO: Remove mock_update_lot_detail and replace with actual mock inserting into DB


@pytest.fixture
def mock_update_lot_detail(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mocks the update_lot_detail function."""
    mock = MagicMock()
    monkeypatch.setattr("apis.v2.routers.files.update_lot_detail", mock)
    return mock


@pytest.mark.parametrize("mock_module", [Module.cai.value, Module.cdc.value])
def test_save_local_success(
    test_client: TestClient,
    mock_module: str,
    sample_lot_details: dict[str, str],
    sample_res_dict: dict[str, str | dict[str, list[str]]],
    mock_set_cache_data: MagicMock,
    mock_update_lot_detail: MagicMock,
) -> None:
    """Tests successful saving of local data."""
    mock_lot_no = sample_lot_details["lotNo"]
    mock_plate = sample_lot_details["plate"]
    mock_item = sample_lot_details["item"]

    response = test_client.post(
        f"/v2/upload/save/{mock_module}/{mock_lot_no}/{mock_plate}/{mock_item}",
        json=sample_res_dict,
    )

    mock_set_cache_data.assert_called_once_with(
        mock_item, sample_res_dict["directory"], sample_res_dict["chips"]
    )
    mock_update_lot_detail.assert_called_once()
    assert response.status_code == 200


@pytest.fixture
def mock_function(
    request: pytest.FixtureRequest,
    mock_set_cache_data: MagicMock,
    mock_update_lot_detail: MagicMock,
) -> MagicMock:
    """Provides sample arguments for exception count retrieval scenarios."""

    return [mock_set_cache_data, mock_update_lot_detail][request.param]


@pytest.mark.parametrize("mock_function", [0, 1], indirect=True)
def test_save_local_exception(
    test_client: TestClient,
    sample_lot_details: dict[str, str],
    sample_res_dict: dict[str, str | dict[str, list[str]]],
    mock_function: MagicMock,
) -> None:

    mock_module = Module.cdc.value
    mock_lot_no = sample_lot_details["lotNo"]
    mock_plate = sample_lot_details["plate"]
    mock_item = sample_lot_details["item"]

    mock_function.side_effect = Exception("Unexpected Error.")

    response = test_client.post(
        f"/v2/upload/save/{mock_module}/{mock_lot_no}/{mock_plate}/{mock_item}",
        json=sample_res_dict,
    )

    mock_function.assert_called_once()
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Bad Request: The request was invalid or cannot be served."
    }


@pytest.fixture
def sample_invalid_args(
    request: pytest.FixtureRequest, sample_lot_details: dict[str, str]
) -> tuple[str, str, str, str]:
    """Provides sample arguments for invalid count retrieval scenarios."""
    lot_no = sample_lot_details["lotNo"]
    plate = sample_lot_details["plate"]
    item = sample_lot_details["item"]

    return [
        ("invalid_module", lot_no, plate, item),
        (Module.cdc.value, "invalid_lot_no", plate, item),
    ][request.param]


@pytest.mark.parametrize("sample_invalid_args", [0, 1], indirect=True)
def test_save_local_invalid(
    test_client: TestClient,
    sample_invalid_args: tuple[str, str, str, str],
    sample_res_dict: dict[str, str | dict[str, list[str]]],
    mock_set_cache_data: MagicMock,
) -> None:

    mock_module, mock_lot_no, mock_plate, mock_item = sample_invalid_args

    response = test_client.post(
        f"/v2/upload/save/{mock_module}/{mock_lot_no}/{mock_plate}/{mock_item}",
        json=sample_res_dict,
    )

    assert response.status_code == 422
    mock_set_cache_data.assert_not_called()
