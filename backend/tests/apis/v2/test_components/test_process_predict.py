import pytest
import numpy as np
from pathlib import Path
from sqlalchemy.orm import Session
from unittest.mock import MagicMock

from apis.v2.components.process_predict import process_n_predict
from apis.v2.schemas.base import CAIPage, CDCPage
from core.directory import directory
from db.models.csam import CSAM_DETAILS


@pytest.fixture
def mock_gray_image():
    """Creates a mock grayscale image."""
    return np.zeros((100, 100), dtype=np.uint8)


@pytest.fixture
def sample_process_dicts(
    mock_gray_image: np.ndarray, sample_chips_batch_details: dict[str, int]
) -> tuple[dict, dict, dict, dict, dict, dict]:
    """Returns sample dictionaries for image processing."""
    count_dict = sample_chips_batch_details
    temp_dict = {f"temp{i}.png": mock_gray_image for i in range(1, 6)}
    ng_dict = {f"ng{i}.png": mock_gray_image for i in range(1, 6)}
    pred_dict = {f"temp{i}.png": mock_gray_image for i in range(1, 6) if i % 2 == 0}

    chip_dict = {
        "batch 1": ["test1.png", "test2.png"],
        "batch 2": ["test3.png", "test4.png"],
    }
    res_dict = {"chips": chip_dict, "directory": ""}

    return count_dict, temp_dict, ng_dict, pred_dict, chip_dict, res_dict


@pytest.fixture
def mock_logger(mock_func_logger: MagicMock) -> MagicMock:
    """Mocks the logger for process prediction."""
    return mock_func_logger("apis.v2.components.process_predict.logger")


@pytest.fixture
def mock_iterdir(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mocks the iterdir function of Path for temp and plate paths."""
    mock = MagicMock()
    monkeypatch.setattr(Path, "iterdir", mock)
    return mock


@pytest.fixture
def mock_process_predict_funcs(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock]:
    """Mocks functions involved in process and prediction workflow."""

    import_path = "apis.v2.components.process_predict."

    mock_initialize = MagicMock()
    mock_get_lot_detail = MagicMock()
    mock_get_cache_data = MagicMock()
    mock_image_process = MagicMock()
    mock_predict_defects = MagicMock()
    mock_thread_write_images = MagicMock()

    monkeypatch.setattr(f"{import_path}initialize", mock_initialize)
    monkeypatch.setattr(f"{import_path}get_lot_detail", mock_get_lot_detail)
    monkeypatch.setattr(f"{import_path}get_cache_data", mock_get_cache_data)
    monkeypatch.setattr(f"{import_path}image_process", mock_image_process)
    monkeypatch.setattr(f"{import_path}predict_defects", mock_predict_defects)
    monkeypatch.setattr(f"{import_path}thread_write_images", mock_thread_write_images)

    return (
        mock_initialize,
        mock_get_lot_detail,
        mock_get_cache_data,
        mock_image_process,
        mock_predict_defects,
        mock_thread_write_images,
    )


@pytest.mark.parametrize(
    "mock_page, mock_iterdir_value",
    [
        (CAIPage, []),
        (CDCPage, []),
        (CAIPage, ["1", "2", "3"]),
        (CDCPage, ["1", "2", "3"]),
    ],
)
def test_process_n_predict_success_new(
    db_session: Session,
    mock_page: CAIPage | CDCPage,
    mock_iterdir_value: list[str | None],
    sample_lot_details: dict[str, str],
    sample_process_dicts: tuple[dict, dict, dict, dict, dict, dict],
    mock_file_methods: tuple[MagicMock, MagicMock],
    mock_process_predict_funcs: tuple[
        MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock
    ],
    mock_iterdir: MagicMock,
):
    """Tests the success scenario of the process_n_predict function."""
    mock_lot_no = sample_lot_details["lotNo"]
    mock_item = sample_lot_details["item"]
    mock_plate = sample_lot_details["plate"]

    count_dict, temp_dict, ng_dict, pred_dict, chip_dict, res_dict = (
        sample_process_dicts
    )
    _, mock_file = mock_file_methods

    (
        mock_initialize,
        mock_get_lot_detail,
        mock_get_cache_data,
        mock_image_process,
        mock_predict_defects,
        mock_thread_write_images,
    ) = mock_process_predict_funcs

    plate_rel_path = (
        f"{mock_page.base_folder}\\{mock_item}\\{mock_lot_no}\\{mock_plate}"
    )
    mock_plate_path = directory.images_dir / plate_rel_path
    mock_temp_path = mock_plate_path / "test_image"

    res_dict["directory"] = plate_rel_path

    mock_iterdir.return_value = mock_iterdir_value
    mock_initialize.return_value = mock_file, mock_plate_path, mock_temp_path
    mock_get_lot_detail.return_value = CSAM_DETAILS
    mock_get_cache_data.return_value = chip_dict
    mock_image_process.return_value = count_dict, temp_dict, ng_dict
    mock_predict_defects.return_value = pred_dict
    mock_thread_write_images.return_value = chip_dict

    result = process_n_predict(mock_lot_no, mock_item, mock_file, db_session, mock_page)

    assert result == res_dict

    mock_initialize.assert_called_once_with(
        mock_lot_no, mock_item, mock_file, directory.images_dir / mock_page.base_folder
    )
    mock_get_lot_detail.assert_called_once_with(
        db_session, mock_lot_no, mock_plate, mock_page.ai
    )
    if not mock_iterdir_value:
        mock_image_process.assert_called_once_with(mock_file, mock_item, mock_page.ai)
        mock_thread_write_images.assert_called_once_with(
            count_dict["no_of_batches"], ng_dict, mock_temp_path, mock_page.ai
        )
        if mock_page.ai:
            mock_predict_defects.assert_called_once_with(mock_item, temp_dict)
