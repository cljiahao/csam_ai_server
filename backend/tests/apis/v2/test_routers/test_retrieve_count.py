import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from apis.v2.schemas.base import Module


# TODO: Remove mock_get_lot_detail and replace with actual mock inserting into DB
@pytest.fixture
def mock_get_lot_detail(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mocks the get_lot_detail function."""
    mock_lot_detail = MagicMock(no_of_pred=100, no_of_chips=50)
    mock_get_lot_detail = MagicMock(return_value=mock_lot_detail)
    monkeypatch.setattr("apis.v2.routers.retrieve.get_lot_detail", mock_get_lot_detail)
    return mock_get_lot_detail


@pytest.mark.parametrize(
    "mock_module, expected_result",
    [
        (Module.cai.value, {"result": 100}),
        (Module.cdc.value, {"result": 50}),
    ],
)
def test_get_processed_count_success(
    test_client: TestClient,
    mock_module: str,
    expected_result: dict[str, int],
    sample_lot_details: dict[str, str],
    mock_get_lot_detail: MagicMock,
) -> None:
    """Tests successful retrieval of processed count."""

    mock_lot_no = sample_lot_details["lotNo"]
    mock_plate = sample_lot_details["plate"]

    response = test_client.get(f"/v2/count/{mock_module}/{mock_lot_no}/{mock_plate}")

    mock_get_lot_detail.assert_called_once()
    assert response.status_code == 200
    assert response.json() == expected_result


def test_get_processed_count_exception(
    test_client: TestClient,
    sample_lot_details: dict[str, str],
    mock_get_lot_detail: MagicMock,
) -> None:
    """Tests exception handling during processed count retrieval."""
    mock_module = Module.cdc.value
    mock_lot_no = sample_lot_details["lotNo"]
    mock_plate = sample_lot_details["plate"]

    mock_get_lot_detail.side_effect = Exception("Unexpected Error")

    response = test_client.get(f"/v2/count/{mock_module}/{mock_lot_no}/{mock_plate}")

    mock_get_lot_detail.assert_called_once()
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

    return [
        ("invalid_module", lot_no, plate),
        (Module.cdc.value, "invalid_lot_no", plate),
    ][request.param]


@pytest.mark.parametrize("sample_invalid_args", [0, 1], indirect=True)
def test_get_processed_count_invalid(
    test_client: TestClient,
    sample_invalid_args: tuple[str, str, str, str],
    mock_get_lot_detail: MagicMock,
) -> None:
    """Tests handling of invalid arguments during count retrieval."""
    mock_module, mock_lot_no, mock_plate = sample_invalid_args

    response = test_client.get(f"/v2/count/{mock_module}/{mock_lot_no}/{mock_plate}")

    assert response.status_code == 422
    mock_get_lot_detail.assert_not_called()
