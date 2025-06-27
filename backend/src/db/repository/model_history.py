from sqlalchemy.orm import Session

from db.models.model_history import ModelHistory
from db.repository.base_repository import BaseRepository


class ModelHistoryRepository(BaseRepository[ModelHistory]):
    def __init__(self, db: Session):
        super().__init__(db, ModelHistory)

    def create_model_history(self, model_history_data: dict) -> list[ModelHistory]:
        """Create new model history."""
        return self.create(
            model_history_data,
            print_message="Error creating new data into ModelHistory database.",
        )

    def read_all_model_history(self, filter_conditions: dict) -> list[ModelHistory]:
        """Read all model history based on filter."""
        return self.read(
            filter_conditions,
            return_all=True,
            print_message="Error reading all data from ModelHistory database.",
        )

    def read_model_history(self, filter_conditions: dict) -> list[ModelHistory]:
        """Read model history based on filter."""
        return self.read(
            filter_conditions,
            print_message="Error reading data from ModelHistory database.",
        )

    def update_model_history(self, update_lists: list[dict[str, dict]]) -> int:
        """Update model history with provided data."""
        return self.update(
            update_lists, print_message="Error updating data in ModelHistory database."
        )

    def delete_model_history(self, filter_conditions: dict) -> int:
        """Delete model history based on filter."""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from ModelHistory database.",
        )
