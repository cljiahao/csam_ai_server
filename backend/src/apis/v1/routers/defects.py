from fastapi import APIRouter

from apis.v1.helpers.HTTPExceptions import handle_exceptions
from apis.v1.schemas.defects import FolderColor
from utils.fileHandle.json import get_colors_json, write_colors_json


router = APIRouter()


@router.get(
    "",
    response_model=FolderColor,
    summary="Retrieve all saved folder settings.",
)
def get_all_folder_colors() -> dict[list[dict[str, str | list[dict[str, str]]]]]:

    try:
        colors_data = get_colors_json()
        return {"colorGroup": colors_data}
    except Exception as e:
        handle_exceptions(e)


@router.get(
    "/{item}",
    response_model=FolderColor,
    summary="Retrieve saved folder settings based on item.",
)
def get_folder_colors(item: str) -> dict[list[dict[str, str | list[dict[str, str]]]]]:

    try:
        colors_data = get_colors_json(item)
        return {"colorGroup": colors_data}
    except Exception as e:
        handle_exceptions(e)


@router.post(
    "",
    summary="Update folder settings.",
)
def set_all_folder_colors(fol_col: FolderColor) -> bool:

    try:
        write_colors_json(fol_col.colorGroup)
        return True
    except Exception as e:
        handle_exceptions(e)


@router.post(
    "/{item}",
    summary="Update folder settings based on item.",
)
def set_folder_colors(item: str, fol_col: FolderColor) -> bool:

    try:
        write_colors_json(fol_col.colorGroup, item)
        return True
    except Exception as e:
        handle_exceptions(e)
