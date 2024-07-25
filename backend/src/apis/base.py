from fastapi import APIRouter

from apis.routes import misc
from apis.routes import CAI_upload
from apis.routes import CAI_database
from apis.routes import CDC_upload
from apis.routes import CDC_database

api_router = APIRouter()

api_router.include_router(misc.router, tags=["misc"])

api_router.include_router(CAI_upload.router, prefix="/CAI", tags=["upload"])
api_router.include_router(CAI_database.router, prefix="/CAI", tags=["db"])

api_router.include_router(CDC_upload.router, prefix="/CDC", tags=["upload"])
api_router.include_router(CDC_database.router, prefix="/CDC", tags=["db"])
