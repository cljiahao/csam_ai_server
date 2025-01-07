from enum import Enum
from fastapi import APIRouter

from apis.v2.routers import colors
from apis.v2.routers import files
from apis.v2.routers import retrieve


class APITag(str, Enum):
    """Enum to define API tags for better organization and documentation."""

    COLORS = "colors"
    FILES = "files"
    RETRIEVE = "retrieve"


router = APIRouter()

router.include_router(colors.router, tags=[APITag.COLORS], prefix="/colors")
router.include_router(files.router, tags=[APITag.FILES], prefix="/upload")
router.include_router(retrieve.router, tags=[APITag.RETRIEVE])
