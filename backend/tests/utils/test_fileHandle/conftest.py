import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_func_read_json(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mock the read_json function."""

    def _mock_func_read_json(read_json_path, value) -> MagicMock:
        mock = MagicMock(return_value=value)
        monkeypatch.setattr(read_json_path, mock)
        return mock

    return _mock_func_read_json


@pytest.fixture
def mock_func_write_json(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mock the write_json function."""

    def _mock_func_write_json(write_json_path) -> MagicMock:
        mock = MagicMock()
        monkeypatch.setattr(write_json_path, mock)
        return mock

    return _mock_func_write_json


@pytest.fixture
def mock_func_settings_json_dependencies(
    sample_lot_details: dict[str, str],
    mock_func_read_json: MagicMock,
    mock_func_write_json: MagicMock,
) -> callable:
    """Provide a fixture to mock settings JSON dependencies."""

    def _mock_func_settings_json_dependencies(
        read_data: dict = None,
    ) -> tuple[MagicMock, MagicMock, MagicMock]:
        mock_item = sample_lot_details["item"]
        mock_read_json = mock_func_read_json(
            "utils.fileHandle.json.read_json", read_data
        )
        mock_write_json = mock_func_write_json("utils.fileHandle.json.write_json")

        return mock_item, mock_read_json, mock_write_json

    return _mock_func_settings_json_dependencies
