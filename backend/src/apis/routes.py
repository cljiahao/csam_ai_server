from fastapi import APIRouter

from apis.v2.routers import base


router = APIRouter()

router.include_router(base.router, prefix="/v2")


@router.get("/health", tags=["health"])
def health():
    return {"status": "OK"}
