import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient


@pytest.fixture
def mock_get_colors_json(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Fixture to mock the get_colors_json function."""
    mock = MagicMock()
    monkeypatch.setattr("apis.v2.routers.defects.get_colors_json", mock)
    return mock


@pytest.fixture
def mock_write_colors_json(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Fixture to mock the write_colors_json function."""
    mock = MagicMock()
    monkeypatch.setattr("apis.v2.routers.defects.write_colors_json", mock)
    return mock


def test_get_colors_json_success(
    test_client: TestClient,
    sample_lot_details: dict[str, str],
    sample_color_group: dict[str, list[dict[str, str]]],
    mock_get_colors_json: MagicMock,
) -> None:
    """Test successful retrieval of colors."""
    sample_item_color = sample_color_group["colorGroup"][0]
    sample_colors = sample_item_color["colors"]
    mock_get_colors_json.return_value = sample_colors

    item = sample_lot_details["item"]
    response = test_client.get(f"/v2/colors/{item}")

    mock_get_colors_json.assert_called_once_with(item)
    assert response.status_code == 200
    assert response.json() == {"colors": sample_colors}


def test_get_colors_json_exception(
    test_client: TestClient,
    sample_lot_details: dict[str, str],
    mock_get_colors_json: MagicMock,
) -> None:
    """Test retrieval of colors when an exception occurs."""
    item = sample_lot_details["item"]

    mock_get_colors_json.side_effect = Exception("Unexpected Error")

    response = test_client.get(f"/v2/colors/{item}")

    mock_get_colors_json.assert_called_once_with(item)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Bad Request: The request was invalid or cannot be served."
    }


def test_write_colors_json_success(
    test_client: TestClient,
    sample_lot_details: dict[str, str],
    sample_color_group: dict[str, list[dict[str, str]]],
    mock_write_colors_json: MagicMock,
) -> None:
    """Test successful writing of colors."""
    item = sample_lot_details["item"]
    sample_item_color = sample_color_group["colorGroup"][0]["colors"]

    response = test_client.post(
        f"/v2/colors/{item}", json={"colors": sample_item_color}
    )

    mock_write_colors_json.assert_called_once()
    assert response.status_code == 200


def test_write_colors_json_exception(
    test_client: TestClient,
    sample_lot_details: dict[str, str],
    sample_color_group: dict[str, list[dict[str, str]]],
    mock_write_colors_json: MagicMock,
) -> None:
    """Test writing colors when an exception occurs."""
    item = sample_lot_details["item"]
    sample_item_color = sample_color_group["colorGroup"][0]["colors"]

    mock_write_colors_json.side_effect = Exception("Unexpected Error")

    response = test_client.post(
        f"/v2/colors/{item}", json={"colors": sample_item_color}
    )

    mock_write_colors_json.assert_called_once()
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Bad Request: The request was invalid or cannot be served."
    }


def test_write_colors_json_invalid(
    test_client: TestClient, sample_lot_details: dict[str, str]
) -> None:
    """Test writing colors with invalid data."""
    item = sample_lot_details["item"]

    response = test_client.post(f"/v2/colors/{item}", json={})

    assert response.status_code == 422
