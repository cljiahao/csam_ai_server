from fastapi import APIRouter

from apis.v2.constants.common import APITags
from apis.v2.routers import ai_model, color_pick, csam_image, stats_data


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


include_tagged_router(ai_model.router, APITags.AI_MODEL)
include_tagged_router(color_pick.router, APITags.COLOR_PICK)
include_tagged_router(csam_image.router, APITags.CSAM_IMAGE)
include_tagged_router(stats_data.router, APITags.STATS_DATA)
