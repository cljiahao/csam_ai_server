import pytest
from unittest.mock import MagicMock

from apis.v2.helpers.pages import get_page
from apis.v2.schemas.base import CAIPage, CDCPage, Module


@pytest.mark.parametrize(
    "module_value, expected_model", [(Module.cai, CAIPage), (Module.cdc, CDCPage)]
)
def test_get_page(module_value: Module, expected_model: type) -> None:
    """Ensure the correct page class is returned based on module value."""
    assert get_page(module_value) is expected_model


def test_get_page_invalid_module(mock_func_logger: MagicMock) -> None:
    """Ensure ValueError is raised for invalid module values and logged."""

    mock_logger = mock_func_logger("apis.v2.helpers.pages.logger")

    mock_module = MagicMock()
    mock_module.value = "invalid"

    with pytest.raises(ValueError) as exc_info:
        get_page(mock_module)

    expected_message = f"Invalid module value: {mock_module}"
    assert str(exc_info.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)
