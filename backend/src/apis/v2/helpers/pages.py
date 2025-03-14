from apis.v2.schemas.base import CAIPage, CDCPage, ServerMode
from core.exceptions import CustomErrorMessage
from utils.debug import error_handler


@error_handler(custom_error=ValueError)
def get_page(server_mode: ServerMode) -> CAIPage | CDCPage:
    """Return the page object based on the module value."""

    if server_mode.value == server_mode.CAI:
        return CAIPage
    elif server_mode.value == server_mode.CDC:
        return CDCPage
    else:
        raise CustomErrorMessage(f"Invalid module value: {server_mode.value}")
