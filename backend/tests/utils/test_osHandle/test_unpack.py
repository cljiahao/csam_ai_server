import zipfile
import pytest
from unittest.mock import MagicMock, mock_open


# TODO: Pytest for unpacking


@pytest.fixture
def sample_zipfile():
    mock_zipfile = MagicMock()
    mock_zipfile.namelist.return_value = ["settings.json", "test.h5", "test.txt"]

    return


@pytest.fixture
def mock_func_zipfile_open(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Fixture to mock zipfile opening."""

    def _mock_func_zipfile_open(read_data: str) -> MagicMock:
        mock_zipfile_open = mock_open(read_data=read_data)
        monkeypatch.setattr(zipfile, "ZipFile", mock_zipfile_open)

        return mock_zipfile_open

    return _mock_func_zipfile_open


def test_unzip_files(mock_zipfile: MagicMock):

    mock_file_open = mock_func_zipfile_open()
