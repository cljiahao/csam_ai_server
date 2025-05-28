from fastapi import APIRouter, Response, status, UploadFile
from fastapi import File, Depends, Query
from sqlalchemy.orm import Session
from typing import Annotated

from apis.v2.logic.ai_model import (
    get_all_model_history,
    get_model_history_by_item,
    install_updated_ai_model,
)
from apis.v2.schemas.ai_model import ModelItemHistory
from core.config import service_settings
from db.session import get_db

router = APIRouter()


@router.get(
    "/model_history",
    response_model=list[ModelItemHistory] | ModelItemHistory,
    summary="Get all model history stored in model folder",
    operation_id="GetModelHistory",
)
def model_history(
    item: Annotated[
        str, Query(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
    db: Annotated[Session, Depends(get_db)],
) -> list[ModelItemHistory] | ModelItemHistory:
    if item:
        return get_model_history_by_item(item, db)
    return get_all_model_history(db)


@router.post(
    "/install_model",
    summary="Install model received",
    operation_id="InstallModel",
    status_code=status.HTTP_204_NO_CONTENT,
)
def install_model(
    item: Annotated[
        str, Query(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
    file_model_label: Annotated[
        UploadFile, File(description="Upload model label file ('.txt')")
    ],
    file_model: Annotated[UploadFile, File(description="Upload model file ('.onnx')")],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    install_updated_ai_model(item, file_model_label, file_model, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
