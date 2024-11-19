from typing import Annotated
from fastapi import Path
from fastapi import APIRouter

from apis.v2.helpers.HTTPExceptions import handle_exceptions
from apis.v2.schemas.defects import ColorGroup, Colors
from utils.fileHandle.json import (
    get_all_colors_json,
    get_colors_json,
    write_all_colors_json,
    write_colors_json,
)


router = APIRouter()


@router.get(
    "",
    response_model=ColorGroup,
    summary="Retrieve all saved folder settings.",
)
def get_all_folder_colors() -> ColorGroup:

    try:
        color_group = get_all_colors_json()
        return {"colorGroup": color_group}
    except Exception as e:
        handle_exceptions(e)


@router.post(
    "",
    summary="Update folder settings.",
)
def set_all_folder_colors(color_group: ColorGroup) -> bool:

    try:
        write_all_colors_json(color_group.model_dump()["colorGroup"])
        return True
    except Exception as e:
        handle_exceptions(e)


@router.get(
    "/{item}",
    response_model=Colors,
    summary="Retrieve saved folder settings based on item.",
)
def get_folder_colors(item: Annotated[str, Path(description="Item Type")]) -> Colors:

    try:
        colors_data = get_colors_json(item)
        return {"colors": colors_data}
    except Exception as e:
        handle_exceptions(e)


@router.post(
    "/{item}",
    summary="Update folder settings based on item.",
)
def set_folder_colors(
    item: Annotated[str, Path(description="Item Type")], colors: Colors
) -> bool:

    try:
        colors_data = [element.model_dump() for element in colors.colors]
        write_colors_json(item, colors_data)
        return True
    except Exception as e:
        handle_exceptions(e)
