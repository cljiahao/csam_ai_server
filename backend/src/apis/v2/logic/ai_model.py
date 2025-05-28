from fastapi import UploadFile
from pathlib import Path
from shutil import copyfileobj
from sqlalchemy.orm import Session

from apis.v2.schemas.ai_model import ModelItemHistory
from constants.tensorflow_model import ModelFiles
from core.directory_manager import directory_manager as dm
from core.logging import logger
from db.services.model_history import ModelHistoryService
from utils.debug import timer


@timer("Retrieve AI Model History by item")
def get_model_history_by_item(item: str, db: Session) -> ModelItemHistory:
    model_history_service = ModelHistoryService(db)
    model_history = model_history_service.read_model_history_not_empty(item)
    return ModelItemHistory(
        id=model_history.id,
        date_install=str(model_history.date_updated),
        item=model_history.item,
        model_name=model_history.file_name,
    )


@timer("Retrieve all AI Model History")
def get_all_model_history(db: Session) -> list[ModelItemHistory]:
    model_history_service = ModelHistoryService(db)
    all_model_history = model_history_service.read_all_model_history()
    return [
        ModelItemHistory(
            id=model_history.id,
            date_install=str(model_history.date_updated),
            item=model_history.item,
            model_name=model_history.file_name,
        )
        for model_history in all_model_history
    ]


@timer("Install AI Model")
def install_updated_ai_model(
    item: str, model_label_file: UploadFile, model_file: UploadFile, db: Session
) -> None:
    # Define file save paths
    model_label_save_path = dm.model_dir / f"{item}{ModelFiles.LABEL_EXT}"
    model_save_path = dm.model_dir / f"{item}{ModelFiles.ONNX_MODEL_EXT}"

    # Save files using extracted function
    save_uploaded_file(model_label_file, model_label_save_path)
    save_uploaded_file(model_file, model_save_path)

    # Update model history in DB
    model_history_service = ModelHistoryService(db)
    model_history_service.create_or_update_model_history(
        item,
        {
            "file_name": model_file.filename,
            "label_file_name": model_label_file.filename,
        },
    )


def save_uploaded_file(file: UploadFile, save_path: Path) -> None:
    """Handles saving an uploaded file and logs errors if the operation fails."""
    try:
        with save_path.open("wb") as f:
            copyfileobj(file.file, f)
    except Exception as e:
        logger.error(f"Error saving file '{file.filename}' to '{save_path}': {e}")
        raise RuntimeError(f"Failed to save file '{file.filename}'") from e
