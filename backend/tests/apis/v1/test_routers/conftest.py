import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_func_handle_exceptions(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Dynamically mock the handle exception method for testing."""

    def _mock_func_handle_execptions(handle_path: str) -> MagicMock:
        """Create a mock for the specified handle path."""
        mock = MagicMock()
        monkeypatch.setattr(handle_path, mock)

        return mock

    return _mock_func_handle_execptions
