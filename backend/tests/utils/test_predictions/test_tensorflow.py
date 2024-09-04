import pytest
import numpy as np
from pathlib import Path
from tensorflow import keras
from unittest.mock import MagicMock
from keras import models

from core.directory import directory
from utils.prediction.tensorflow_model import load_model, run_CNN


@pytest.fixture
def mock_exists(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mocks the Path.exists method."""

    mock_exists = MagicMock(return_value=True)
    monkeypatch.setattr(Path, "exists", mock_exists)

    return mock_exists


@pytest.fixture
def mock_load_model(monkeypatch: pytest.MonkeyPatch) -> MagicMock:

    mock_load_model = MagicMock()
    monkeypatch.setattr(models, "load_model", mock_load_model)

    return mock_load_model


def test_load_model_success(
    sample_lot_details: dict[str, str | int], mock_logging: MagicMock
):

    mock_logger = mock_logging("utils.predcitions.tensorflow_model.logger")
    lot_no = sample_lot_details["lotNo"]

    result = load_model(lot_no)

    model_path = directory.model_dir / f"{lot_no}.h5"
    mock_logger.info.assert_called_once_with(f"Model loaded from {model_path}")


def test_load_model_not_exists(
    sample_lot_details: dict[str, str | int],
    mock_logging: MagicMock,
    mock_exists: MagicMock,
):

    mock_logger = mock_logging("utils.predcitions.tensorflow_model.logger")
    mock_exists.result_value = False

    lot_no = sample_lot_details["lotNo"]

    with pytest.raises(FileNotFoundError) as exc_info:
        load_model(lot_no)

    model_f_name = f"{lot_no}.h5"
    expected_message = f"Model File: {model_f_name} not found in model folder"
    assert str(exc_info.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)


@pytest.fixture
def mock_np_modules(monkeypatch: pytest.MonkeyPatch) -> tuple[MagicMock, MagicMock]:

    mock_array = MagicMock()
    mock_argmax = MagicMock()

    monkeypatch.setattr(np, "array", mock_array)
    monkeypatch.setattr(np, "argmax", mock_argmax)

    return mock_array, mock_argmax


@pytest.fixture
def mock_g_constant(monkeypatch: pytest.MonkeyPatch) -> MagicMock:

    mock_g_constants = MagicMock()
    mock_g_constants.G_TYPES = ["G"]
    monkeypatch.setattr("core.constants", mock_g_constants)

    return mock_g_constants


def test_run_CNN(mock_labels: dict[str, str]):

    mock_model = MagicMock()
    mock_model.predict = MagicMock()

    run_CNN(
        mock_model,
        mock_labels,
    )
