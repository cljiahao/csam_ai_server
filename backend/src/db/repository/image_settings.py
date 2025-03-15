from sqlalchemy.orm import Session

from db.models.image_settings import ImageSettings
from db.repository.base_repository import BaseRepository


class ImageSettingsRepository(BaseRepository[ImageSettings]):
    def __init__(self, db: Session):
        super().__init__(db, ImageSettings)

    def create_image_settings(self, settings_data: dict) -> ImageSettings:
        """Create new image settings."""
        return self.create(
            settings_data,
            print_message=f"Error creating settings from the database.",
        )

    def read_image_settings(self, filter_conditions: dict) -> ImageSettings:
        """Read image settings based on filter."""
        return self.read(
            filter_conditions,
            print_message=f"Error reading settings from the database.",
        )

    def update_image_settings(
        self, filter_conditions: dict, update_data: dict
    ) -> ImageSettings:
        """Update image settings with provided data."""
        return self.update(
            filter_conditions,
            update_data,
            print_message=f"Error updating settings in the database.",
        )

    def delete_image_settings(self, filter_conditions: dict) -> ImageSettings:
        """Delete image settings based on filter."""
        return self.delete(
            filter_conditions,
            print_message=f"Error deleting settings from the database.",
        )
