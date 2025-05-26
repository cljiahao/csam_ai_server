from fastapi import APIRouter

from apis.v2.constants.common import APITags


router = APIRouter()


@router.get(
    "/health",
    tags=["health"],
    summary="Health Check",
    description="A simple health check returning a OK status.",
)
def v2_health():
    return {"status": "OK"}


def include_tagged_router(sub_router, tag: APITags) -> None:
    """Includes a sub-router with a tag and a prefix derived from the tag's value."""
    router.include_router(sub_router, tags=[tag], prefix=f"/{tag.value}")
