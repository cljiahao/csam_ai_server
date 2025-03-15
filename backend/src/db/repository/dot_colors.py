from sqlalchemy.orm import Session

from db.models.dot_colors import DotColors
from db.repository.base_repository import BaseRepository


class DotColorsRepository(BaseRepository[DotColors]):
    def __init__(self, db: Session):
        super().__init__(db, DotColors)

    def bulk_create_dot_colors(self, dot_colors_list: list[dict]) -> DotColors:
        """Create new dot colors details."""
        return self.create(
            dot_colors_list,
            print_message=f"Error creating dot colors details from the database.",
        )

    def read_all_dot_colors(self, filter_conditions: dict) -> list[DotColors]:
        """Read all colors details details based on filter."""
        return self.read(
            filter_conditions,
            return_all=True,
            print_message=f"Error reading dot colors details from the database.",
        )

    def bulk_update_dot_colors(self, updates_list: list[dict[str, dict]]) -> DotColors:
        """Update dot colors details with provided data."""
        return self.update(
            updates_list,
            print_message=f"Error updating dot colors details in the database.",
        )

    def bulk_delete_dot_colors(self, filter_conditions: list[dict]) -> DotColors:
        """Delete dot colors details based on filter."""
        return self.delete(
            filter_conditions,
            print_message=f"Error deleting dot colors details from the database.",
        )
