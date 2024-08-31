from fastapi import APIRouter

from apis.v1.routers import base


router = APIRouter()

router.include_router(base.router, prefix="/v1")


@router.get("/health", tags=["health"])
def health():
    return {"status": "OK"}
