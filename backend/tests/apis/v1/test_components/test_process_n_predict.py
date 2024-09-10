import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_logger(mock_func_logger: MagicMock) -> MagicMock:
    return mock_func_logger("apis.v1.components.process_predict.logger")


# @pytest.mark.skip
# def test_process_n_predict_success(mock_logger: MagicMock):


#     mock_logger.error.
