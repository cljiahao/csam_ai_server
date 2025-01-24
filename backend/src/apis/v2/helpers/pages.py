from apis.v2.schemas.base import CAIPage, CDCPage, Module
from core.exceptions import CustomErrorMessage
from utils.debug import error_handler


@error_handler(custom_error=ValueError)
def get_page(module: Module) -> CAIPage | CDCPage:
    """Return the page object based on the module value."""

    if module.value == module.cai:
        return CAIPage
    elif module.value == module.cdc:
        return CDCPage
    else:
        raise CustomErrorMessage(f"Invalid module value: {module.value}")
