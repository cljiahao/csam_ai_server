from fastapi import APIRouter

from apis.routes import CAI_upload
from apis.routes import CAI_db
from apis.routes import CDC_upload
from apis.routes import CDC_db
from apis.routes import CDC_save
from apis.routes import Settings_adjust
from apis.routes import Settings_folders


api_router = APIRouter()
api_router.include_router(CAI_upload.router, prefix="/CAI", tags=["upload"])
api_router.include_router(CAI_db.router, prefix="/CAI", tags=["db"])


api_router.include_router(CDC_upload.router, prefix="/CDC", tags=["upload"])
api_router.include_router(CDC_db.router, prefix="/CDC", tags=["db"])
api_router.include_router(CDC_save.router, prefix="/CDC", tags=["save"])

api_router.include_router(Settings_folders.router, prefix="/Settings", tags=["folders"])
api_router.include_router(Settings_adjust.router, prefix="/Settings", tags=["adjust"])
