from fastapi import APIRouter

from apis.v2.routers import base


router = APIRouter()

router.include_router(base.router, prefix="/v2")


@router.get(
    "/",
    tags=["home"],
    summary="Home Route",
    description="A simple home route returning a welcome message.",
)
def home() -> dict[str, str]:
    """Simple home route."""
    return {"msg": "Hello Fast_API 🚀"}
