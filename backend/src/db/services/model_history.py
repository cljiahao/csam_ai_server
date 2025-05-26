from sqlalchemy.orm import Session

from core.exceptions import InvalidInputError
from db.models.model_history import ModelHistory
from db.repository.model_history import ModelHistoryRepository


class ModelHistoryService:
    def __init__(self, db: Session):
        """Initialize service with repository."""
        self.repo = ModelHistoryRepository(db)

    def _validate_model_history_keys(self, model_history_data: dict) -> None:
        """Validate the keys in the model history data."""
        valid_keys = {
            "file_name",
            "label_file_name",
        }

        invalid_keys = set(model_history_data) - valid_keys
        if invalid_keys:
            raise InvalidInputError(
                f"Unknown keys in model history data: {', '.join(invalid_keys)}"
            )

    def read_all_model_history(self, item: str) -> list[ModelHistory]:
        """Service layer method to read all model history"""
        if not item:
            raise InvalidInputError("Item cannot be empty.")
        filter_conditions = {"item": item}

        return self.repo.read_all_model_history(filter_conditions)

    def read_model_history(self, item: str) -> ModelHistory:
        """Service layer method to read model history"""
        if not item:
            raise InvalidInputError("Item cannot be empty.")
        filter_conditions = {"item": item}

        return self.repo.read_model_history(filter_conditions)[0]

    def create_or_update_model_history(
        self, item: str, model_history_data: dict[str, int]
    ) -> ModelHistory | int:
        """Service layer method to create new or update model history"""
        if not item:
            raise InvalidInputError("Item cannot be empty.")

        self._validate_model_history_keys(model_history_data)

        data_condition = {"item": item}

        existing_settings = self.read_model_history(item)
        if existing_settings:
            self.repo.update_model_history(
                {"filter_conditions": data_condition, "update_data": model_history_data}
            )
            return self.read_model_history(item)

        model_history_data.update(data_condition)
        return self.repo.create_model_history(model_history_data)[0]
