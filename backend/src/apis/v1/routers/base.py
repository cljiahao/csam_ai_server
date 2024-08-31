from enum import Enum
from fastapi import APIRouter

from apis.v1.routers import defects
from apis.v1.routers import files
from apis.v1.routers import retrieve


class APITag(str, Enum):
    """Enum to define API tags for better organization and documentation."""

    DEFECTS = "defects"
    FILES = "files"
    RETRIEVE = "retrieve"


router = APIRouter()

router.include_router(defects.router, tags=[APITag.DEFECTS], prefix="/fol_color")
router.include_router(files.router, tags=[APITag.FILES], prefix="/upload")
router.include_router(retrieve.router, tags=[APITag.RETRIEVE])
