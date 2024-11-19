import pytest
import numpy as np
from pathlib import Path
from tensorflow import keras
from unittest.mock import MagicMock
from keras import models

from core.directory import directory
from utils.prediction.tensorflow_model import load_model, run_CNN


@pytest.fixture
def mock_logger(mock_func_logger: MagicMock) -> MagicMock:
    return mock_func_logger("utils.prediction.tensorflow_model.logger")


@pytest.fixture
def mock_exists(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mocks the Path.exists method."""

    mock = MagicMock(return_value=True)
    monkeypatch.setattr(Path, "exists", mock)
    return mock


@pytest.fixture
def mock_load_model(monkeypatch: pytest.MonkeyPatch) -> MagicMock:

    mock = MagicMock()
    monkeypatch.setattr(models, "load_model", mock)
    return mock


def test_load_model_success(
    sample_lot_details: dict[str, str],
    mock_exists: MagicMock,
    mock_load_model: MagicMock,
    mock_logger: MagicMock,
):

    item = sample_lot_details["item"]

    result = load_model(item)

    mock_exists.assert_called_once()
    model_path = directory.model_dir / f"{item}.h5"
    mock_load_model.assert_called_once_with(model_path)
    mock_logger.info.assert_called_once_with(f"Model loaded from {model_path}")


def test_load_model_not_exists(
    sample_lot_details: dict[str, str],
    mock_logger: MagicMock,
    mock_exists: MagicMock,
):

    mock_exists.return_value = False

    item = sample_lot_details["item"]

    with pytest.raises(FileNotFoundError) as exc_info:
        load_model(item)

    model_f_name = f"{item}.h5"
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

    mock = MagicMock()
    mock.G_TYPES = ["G"]
    monkeypatch.setattr("core.constants", mock)
    return mock


@pytest.mark.skip("Need to create samples for how prediction looks like.")
def test_run_CNN(mock_labels: dict[str, str]):

    mock_model = MagicMock()
    mock_model.predict = MagicMock()

    run_CNN(
        mock_model,
        mock_labels,
    )
