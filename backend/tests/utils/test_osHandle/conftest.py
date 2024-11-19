import cv2
import pytest
import numpy as np
from unittest.mock import MagicMock


@pytest.fixture
def mock_cv2_methods(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[MagicMock, MagicMock, MagicMock, MagicMock]:
    """Fixture to mock cv2 methods."""

    mock_image = np.zeros((2, 2, 3), dtype=np.uint8)

    mock_cvtColor = MagicMock(return_value=mock_image)
    mock_imdecode = MagicMock(return_value=mock_image)
    mock_imwrite = MagicMock()

    monkeypatch.setattr(cv2, "cvtColor", mock_cvtColor)
    monkeypatch.setattr(cv2, "imdecode", mock_imdecode)
    monkeypatch.setattr(cv2, "imwrite", mock_imwrite)

    return mock_image, mock_cvtColor, mock_imdecode, mock_imwrite
