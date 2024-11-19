import pytest
import requests
from unittest.mock import MagicMock

from utils.services.prass import check_lot

LOT_COLUMN = "lot"
ITEM_COLUMN = "item"
PRASS_URL = "http://mock_prass_url/data?lotNo="

module_path = "utils.services.prass"


@pytest.fixture
def mock_logger(mock_func_logger: MagicMock) -> MagicMock:
    """Mock logger for HTTPExceptions."""
    return mock_func_logger(f"{module_path}.logger")


@pytest.fixture
def mock_env(
    monkeypatch: pytest.MonkeyPatch, sample_lot_details: dict[str, str]
) -> None:
    """Setup environment variables for the PRASS service."""

    service_settings = f"{module_path}.service_settings"
    monkeypatch.setattr(f"{service_settings}.TEST_LOT_NO", sample_lot_details["lotNo"])
    monkeypatch.setattr(f"{service_settings}.TEST_ITEM", sample_lot_details["item"])
    monkeypatch.setattr(f"{service_settings}.LOT_COLUMN", LOT_COLUMN)
    monkeypatch.setattr(f"{service_settings}.ITEM_COLUMN", ITEM_COLUMN)
    monkeypatch.setattr(f"{service_settings}.PRASS_URL", PRASS_URL)


@pytest.fixture
def mock_func_get_service(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mock requests.get used by check_lot."""

    def _mock_func_get_service(lot_no: str, item: str) -> MagicMock:
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {LOT_COLUMN: lot_no, ITEM_COLUMN: item}

        mock_request = MagicMock(return_value=mock_response)
        monkeypatch.setattr(requests, "get", mock_request)

        return mock_request

    return _mock_func_get_service


def test_check_lot_success(mock_func_get_service: MagicMock, mock_env: None) -> None:
    """Test check_lot for successful lot lookup."""

    lot_no = "lot_success"
    item = "item_success"

    mock_request_get = mock_func_get_service(lot_no, item)
    result = check_lot(lot_no)

    assert result == item
    mock_request_get.assert_called_once_with(f"{PRASS_URL}{lot_no}")


def test_check_lot_test_success(
    sample_lot_details: dict[str, str], mock_env: None
) -> None:
    """Test check_lot using test lot number."""

    result = check_lot(sample_lot_details["lotNo"])
    assert result == sample_lot_details["item"]


def test_check_lot_url_missing(
    monkeypatch: pytest.MonkeyPatch, mock_logger: MagicMock, mock_env: None
) -> None:
    """Test check_lot when PRASS URL is missing."""

    monkeypatch.setattr(f"{module_path}.service_settings.PRASS_URL", None)
    result = check_lot("url_missing")

    assert result is None
    mock_logger.error.assert_called_once_with("PRASS URL is not configured.")


def test_check_lot_not_exists(
    mock_logger: MagicMock, mock_func_get_service: MagicMock, mock_env: None
) -> None:
    """Test check_lot when lot does not exist."""

    lot_no = "lot_not_exists"

    mock_func_get_service(None, None)
    with pytest.raises(ValueError) as exc_info:
        check_lot(lot_no)

    expected_message = f"Lot number: {lot_no} not found in PRASS Server."
    assert str(exc_info.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)


def test_check_lot_invalid(
    mock_logger: MagicMock, mock_func_get_service: MagicMock, mock_env: None
) -> None:
    """Test check_lot with invalid request."""

    lot_no = "invalid_request"

    mock_request_get = mock_func_get_service(None, None)
    mock_request_get.side_effect = requests.RequestException("Not Found")

    with pytest.raises(requests.RequestException) as exc_info:
        check_lot(lot_no)

    mock_request_get.assert_called_once_with(f"{PRASS_URL}{lot_no}")
    expected_message = f"Error fetching data from PRASS server: {exc_info.value}"
    mock_logger.error.assert_called_once_with(expected_message)
