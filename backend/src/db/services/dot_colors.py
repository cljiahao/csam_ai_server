from uuid import UUID
from sqlalchemy.orm import Session

from core.exceptions import InvalidInputError
from db.models.dot_colors import DotColors
from db.repository.dot_colors import DotColorsRepository


class DotColorsService:
    def __init__(self, db: Session):
        """Initialize service with repository."""
        self.repo = DotColorsRepository(db)

    def _validate_dot_colors_keys(self, dot_colors_data: dict) -> None:
        """Validate the keys in the dot colors data."""
        valid_keys = {
            "defect_label",
            "hex_color",
            "item",
            "uuid",
        }

        invalid_keys = set(dot_colors_data) - valid_keys
        if invalid_keys:
            raise InvalidInputError(
                f"Unknown keys in dot colors data: {', '.join(invalid_keys)}"
            )

    def bulk_create_dot_colors(
        self, dot_color_list: list[dict[str, str]]
    ) -> list[DotColors]:
        """Service layer method to bulk create dot colors"""
        for dot_colors in dot_color_list:
            self._validate_dot_colors_keys(dot_colors)

        return self.repo.bulk_create_dot_colors(dot_color_list)

    def read_all_dot_colors(self, item: str) -> list[DotColors]:
        """Service layer method to read all dot colors"""
        if not item:
            raise InvalidInputError("Item cannot be empty.")
        filter_conditions = {"item": item}

        return self.repo.read_all_dot_colors(filter_conditions)

    # TODO: create update_list here instead
    def bulk_update_dot_colors(self, update_list: list[dict[str, dict]]) -> int:
        """Service layer method to bulk update dot colors"""
        for update_item in update_list:
            self._validate_dot_colors_keys(update_item["update_data"])

        return self.repo.bulk_update_dot_colors(update_list)

    def bulk_delete_dot_colors(self, uuid_list: list[UUID]) -> int:
        """Service layer method to bulk delete dot colors by uuid."""
        if not uuid_list:
            return 0
        filter_conditions = [{"uuid": uuid} for uuid in uuid_list]

        return self.repo.bulk_delete_dot_colors(filter_conditions)
