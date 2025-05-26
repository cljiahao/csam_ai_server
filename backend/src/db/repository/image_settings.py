from sqlalchemy.orm import Session

from db.models.image_settings import ImageSettings
from db.repository.base_repository import BaseRepository


class ImageSettingsRepository(BaseRepository[ImageSettings]):
    def __init__(self, db: Session):
        super().__init__(db, ImageSettings)

    def create_image_settings(self, settings_data: dict) -> list[ImageSettings]:
        """Create new image settings."""
        return self.create(
            settings_data,
            print_message="Error creating new data into ImageSettings database.",
        )

    def read_image_settings(self, filter_conditions: dict) -> list[ImageSettings]:
        """Read image settings based on filter."""
        return self.read(
            filter_conditions,
            print_message="Error reading data from ImageSettings database.",
        )

    def update_image_settings(self, update_lists: list[dict[str, dict]]) -> int:
        """Update image settings with provided data."""
        return self.update(
            update_lists,
            print_message="Error updating data in ImageSettings database.",
        )

    def delete_image_settings(self, filter_conditions: dict) -> int:
        """Delete image settings based on filter."""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from ImageSettings database.",
        )
