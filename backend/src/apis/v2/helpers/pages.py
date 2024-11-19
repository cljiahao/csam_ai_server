from apis.v2.schemas.base import CAIPage, CDCPage, Module
from core.logging import logger


def get_page(module: Module) -> CAIPage | CDCPage:
    """Return the page object based on the module value."""

    if module.value == module.cai:
        return CAIPage
    elif module.value == module.cdc:
        return CDCPage

    std_out = f"Invalid module value: {module}"
    logger.error(std_out)
    raise ValueError(std_out)
