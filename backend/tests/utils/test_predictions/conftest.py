import pytest


@pytest.fixture
def sample_labels() -> dict[str, str]:
    return {
        "0": "G",
        "1": "NG",
        "2": "Sides",
        "3": "AirBubble",
    }


@pytest.fixture
def sample_pred_dict():
    return {
        "file_name": [0, 0, 0],
        "file_name": [0, 0, 0],
        "file_name": [0, 0, 0],
        "file_name": [0, 0, 0],
    }


@pytest.fixture
def sample_pred_res():
    return
