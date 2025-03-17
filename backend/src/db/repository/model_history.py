from sqlalchemy.orm import Session

from db.models.model_history import ModelHistory
from db.repository.base_repository import BaseRepository


class ModelHistoryRepository(BaseRepository[ModelHistory]):
    def __init__(self, db: Session):
        super().__init__(db, ModelHistory)

    def create_model_history(self, model_history_data: dict) -> ModelHistory:
        """Create new model history details."""
        return self.create(
            model_history_data,
            print_message=f"Error creating model history details from the database.",
        )

    def read_all_model_history(self, filter_conditions: dict) -> list[ModelHistory]:
        """Read all model history details based on filter."""
        return self.read(
            filter_conditions,
            return_all=True,
            print_message=f"Error reading model history details from the database.",
        )

    def read_model_history(self, filter_conditions: dict) -> ModelHistory:
        """Read model history details based on filter."""
        return self.read(
            filter_conditions,
            print_message=f"Error reading model history details from the database.",
        )

    def update_model_history(self, updates_list: list[dict[str, dict]]) -> ModelHistory:
        """Update model history details with provided data."""
        return self.update(
            updates_list,
            print_message=f"Error updating model history details in the database.",
        )

    def delete_model_history(self, filter_conditions: dict) -> ModelHistory:
        """Delete model history details based on filter."""
        return self.delete(
            filter_conditions,
            print_message=f"Error deleting model history details from the database.",
        )
