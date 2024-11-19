import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient


@pytest.fixture
def mock_func_check_lot(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Fixture that mocks the check_lot method."""

    def _mock_func_check_lot(item: str = "") -> MagicMock:
        mock = MagicMock(return_value=item)
        monkeypatch.setattr("apis.v2.routers.retrieve.check_lot", mock)
        return mock

    return _mock_func_check_lot


@pytest.fixture
def sample_lot_no_item(
    request: pytest.FixtureRequest, sample_lot_details: dict[str, str]
) -> tuple[str, str]:
    """Fixture that returns a tuple of (lotNo, item) based on the request parameter."""

    lot_no_item_pairs = [
        (sample_lot_details["lotNo"], sample_lot_details["item"]),
        (sample_lot_details["lotNo"], ""),
    ]
    return lot_no_item_pairs[request.param]


@pytest.mark.parametrize("sample_lot_no_item", [0, 1], indirect=True)
def test_get_item_success(
    test_client: TestClient,
    mock_func_check_lot: MagicMock,
    sample_lot_no_item: tuple[str, str],
) -> None:
    """Test successful retrieval of an item."""

    lot_no, item = sample_lot_no_item
    mock_check_lot = mock_func_check_lot(item)

    response = test_client.get(f"/v2/item/{lot_no}")

    mock_check_lot.assert_called_once_with(lot_no)
    assert response.status_code == 200
    assert response.json() == {"item": item}


def test_get_item_exception(
    test_client: TestClient, mock_func_check_lot: MagicMock
) -> None:
    """Test retrieval of an item when an exception is raised."""

    lot_no = "failure123"
    mock_check_lot = mock_func_check_lot()
    mock_check_lot.side_effect = Exception("Not Found")

    response = test_client.get(f"/v2/item/{lot_no}")

    mock_check_lot.assert_called_once_with(lot_no)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Bad Request: The request was invalid or cannot be served."
    }


def test_get_item_invalid(test_client: TestClient) -> None:
    """Test retrieval of an item with an invalid lot number."""

    lot_no = "invalid"

    response = test_client.get(f"/v2/item/{lot_no}")

    assert response.status_code == 422
