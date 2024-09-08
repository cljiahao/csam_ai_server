import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from apis.v1.schemas.base import CAIPage, CDCPage, Module


@pytest.fixture
def mock_exception(mock_func_handle_exceptions: MagicMock):

    def raise_http_exception(e: Exception) -> None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid module specified",
        ) from e

    mock_handle_exceptions = mock_func_handle_exceptions(
        "apis.v1.routers.retrieve.handle_exceptions"
    )
    mock_handle_exceptions.side_effect = raise_http_exception

    return mock_handle_exceptions


@pytest.fixture
def mock_get_page(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mocks the get_page function."""

    mock_page = MagicMock()
    mock_page.return_value = MagicMock()
    monkeypatch.setattr("apis.v1.routers.retrieve.get_page", mock_page)

    return mock_page


@pytest.fixture
def mock_get_lot_detail(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mocks the get_lot_detail function."""

    mock_lot_detail = MagicMock(no_of_pred=100, no_of_chips=50)
    mock_get_lot_detail = MagicMock(return_value=mock_lot_detail)
    monkeypatch.setattr("apis.v1.routers.retrieve.get_lot_detail", mock_get_lot_detail)

    return mock_get_lot_detail


@pytest.fixture
def sample_retrieve_args(
    request: pytest.FixtureRequest, sample_lot_details: dict[str, str | int]
) -> tuple[Module, str, str, str, dict[str, int]]:
    """Provides sample (lotNo, item) tuples."""

    lot_no = sample_lot_details["lotNo"]
    plate = sample_lot_details["plate"]

    retrieve_args = [
        (Module.cai.value, CAIPage, lot_no, plate, {"result": 100}),
        (Module.cdc.value, CDCPage, lot_no, plate, {"result": 50}),
    ]
    return retrieve_args[request.param]


@pytest.mark.parametrize("sample_retrieve_args", [0, 1], indirect=True)
def test_get_processed_count_success(
    test_client: TestClient,
    mock_get_page: MagicMock,
    mock_get_lot_detail: MagicMock,
    sample_retrieve_args: tuple[Module, str, str, str, dict[str, int]],
) -> None:
    """Test the successful retrieval of processed count."""

    module, model, lot_no, plate, expected_result = sample_retrieve_args
    mock_get_page.return_value = model

    response = test_client.get(f"/v1/count/{module}/{lot_no}/{plate}")

    assert response.status_code == 200
    assert response.json() == expected_result
    mock_get_page.assert_called_once_with(module)
    mock_get_lot_detail.assert_called_once()


def test_get_processed_count_exception(
    test_client: TestClient,
    mock_get_page: MagicMock,
    mock_exception: MagicMock,
) -> None:
    """Test exception handling when retrieving processed count."""

    mock_get_page.side_effect = Exception("Unexpected error")

    response = test_client.get(f"/v1/count/CAI/1234567890/plate")

    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid module specified"}
    mock_exception.assert_called_once()


def test_get_processed_count_invalid_module(
    test_client: TestClient,
) -> None:
    """Test invalid module handling in count retrieval."""

    response = test_client.get(f"/v1/count/invalid_module/1234567890/plate")

    assert response.status_code == 422
