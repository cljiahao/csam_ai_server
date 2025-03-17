from pathlib import Path
from shutil import copyfileobj
from fastapi import UploadFile
from sqlalchemy.orm import Session

from core.directory_manager import directory_manager as dm
from core.logging import logger
from db.services.model_history import ModelHistoryService


def save_uploaded_file(file: UploadFile, save_path: Path) -> None:
    """Handles saving an uploaded file and logs errors if the operation fails."""
    try:
        with save_path.open("wb") as f:
            copyfileobj(file.file, f)
    except Exception as e:
        logger.error(f"Error saving file '{file.filename}' to '{save_path}': {e}")
        raise RuntimeError(f"Failed to save file '{file.filename}'") from e


def save_model_files(
    item: str, model_label_file: UploadFile, model_file: UploadFile, db: Session
) -> bool:

    # Define file save paths
    model_label_save_path = (
        dm.model_dir / f"{item}{Path(model_label_file.filename).suffix}"
    )
    model_save_path = dm.model_dir / f"{item}{Path(model_file.filename).suffix}"

    # Save files using extracted function
    save_uploaded_file(model_label_file, model_label_save_path)
    save_uploaded_file(model_file, model_save_path)

    # Update model history in DB
    model_history_service = ModelHistoryService(db)
    model_history_service.create_or_update_model_history(
        item,
        {
            "ai_model_name": model_file.filename,
            "model_label_file_name": model_label_file.filename,
        },
    )

    return True
