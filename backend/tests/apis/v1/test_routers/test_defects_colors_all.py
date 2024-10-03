import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient


@pytest.fixture
def mock_get_all_colors_json(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Fixture to mock the get_all_colors_json function."""
    mock = MagicMock()
    monkeypatch.setattr("apis.v2.routers.defects.get_all_colors_json", mock)
    return mock


@pytest.fixture
def mock_write_all_colors_json(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Fixture to mock the write_all_colors_json function."""
    mock = MagicMock()
    monkeypatch.setattr("apis.v2.routers.defects.write_all_colors_json", mock)
    return mock


def test_get_all_colors_json_success(
    test_client: TestClient,
    sample_color_group: dict[str, list[dict[str, str]]],
    mock_get_all_colors_json: MagicMock,
) -> None:
    """Test successful retrieval of all colors."""
    mock_get_all_colors_json.return_value = sample_color_group["colorGroup"]

    response = test_client.get("/v2/colors")

    mock_get_all_colors_json.assert_called_once()
    assert response.status_code == 200
    assert response.json() == sample_color_group


def test_get_all_colors_json_exception(
    test_client: TestClient, mock_get_all_colors_json: MagicMock
) -> None:
    """Test retrieval of all colors when an exception occurs."""
    mock_get_all_colors_json.side_effect = Exception("Unexpected Error")

    response = test_client.get("/v2/colors")

    mock_get_all_colors_json.assert_called_once()
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Bad Request: The request was invalid or cannot be served."
    }


def test_write_all_colors_json_success(
    test_client: TestClient,
    sample_color_group: dict[str, list[dict[str, str]]],
    mock_write_all_colors_json: MagicMock,
) -> None:
    """Test successful writing of all colors."""
    response = test_client.post("/v2/colors", json=sample_color_group)

    mock_write_all_colors_json.assert_called_once()
    assert response.status_code == 200


def test_write_all_colors_json_exception(
    test_client: TestClient,
    sample_color_group: dict[str, list[dict[str, str]]],
    mock_write_all_colors_json: MagicMock,
) -> None:
    """Test writing of all colors when an exception occurs."""
    mock_write_all_colors_json.side_effect = Exception("Unexpected Error")

    response = test_client.post("/v2/colors", json=sample_color_group)

    mock_write_all_colors_json.assert_called_once()
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Bad Request: The request was invalid or cannot be served."
    }


def test_write_all_colors_json_invalid(test_client: TestClient) -> None:
    """Test writing of colors with invalid data."""
    response = test_client.post("/v2/colors", json={})

    assert response.status_code == 422
