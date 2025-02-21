from sqlalchemy.orm import Session

from db.models.image_settings import ImageSettings
from db.repository.base_repository import BaseRepository


class ImageSettingsRepository(BaseRepository[ImageSettings]):
    def __init__(self, db: Session):
        super().__init__(db, ImageSettings)

    def create_settings(self, settings_data: dict) -> ImageSettings:
        """Create new chip settings."""
        return self.create(
            settings_data,
            print_message=f"Error creating settings from the database.",
        )

    def read_settings(self, filter_condition: dict) -> ImageSettings:
        """Read chip settings based on filter."""
        return self.read(
            filter_condition,
            print_message=f"Error reading settings from the database.",
        )

    def update_settings(
        self, filter_condition: dict, update_data: dict
    ) -> ImageSettings:
        """Update chip settings with provided data."""
        return self.update(
            filter_condition,
            update_data,
            print_message=f"Error updating settings in the database.",
        )

    def delete_settings(self, filter_condition: dict) -> ImageSettings:
        """Delete chip settings based on filter."""
        return self.delete(
            filter_condition,
            print_message=f"Error deleting settings from the database.",
        )
