from sqlalchemy.orm import Session

from db.models.dot_colors import DotColors
from db.repository.base_repository import BaseRepository


class DotColorsRepository(BaseRepository[DotColors]):
    def __init__(self, db: Session):
        super().__init__(db, DotColors)

    def bulk_create_dot_colors(self, dot_colors_list: list[dict]) -> list[DotColors]:
        """Bulk create new dot colors."""
        return self.create(
            dot_colors_list,
            print_message="Error creating new data into DotColors database.",
        )

    def read_all_dot_colors(self, filter_conditions: dict) -> list[DotColors]:
        """Read all dot colors based on filter."""
        return self.read(
            filter_conditions,
            return_all=True,
            print_message="Error reading all data from DotColors database.",
        )

    def bulk_update_dot_colors(self, update_lists: list[dict[str, dict]]) -> int:
        """Bulk update dot colors with provided data."""
        return self.update(
            update_lists, print_message="Error updating data in DotColors database."
        )

    def bulk_delete_dot_colors(self, filter_conditions: list[dict]) -> int:
        """Bulk delete dot colors based on filter."""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from DotColors database.",
        )
