from sqlalchemy.orm import Session

from core.exceptions import InvalidInputError
from db.models.image_settings import ImageSettings
from db.repository.image_settings import ImageSettingsRepository


class ImageSettingsService:
    def __init__(self, db: Session):
        """Initialize service with repository."""
        self.repo = ImageSettingsRepository(db)

    def _validate_image_settings_keys(self, image_settings_data: dict) -> None:
        """Validate the keys in the image settings data."""
        valid_keys = {
            "batch_erode",
            "batch_close",
            "chip_erode",
            "chip_close",
            "crop_size",
        }

        invalid_keys = set(image_settings_data) - valid_keys
        if invalid_keys:
            raise InvalidInputError(
                f"Unknown keys in image settings data: {', '.join(invalid_keys)}"
            )

    def read_image_settings(self, item: str) -> ImageSettings:
        """Service layer method to read image settings"""
        if not item:
            raise InvalidInputError("Item cannot be empty.")
        filter_condition = {"item": item}

        return self.repo.read_image_settings(filter_condition)

    def create_or_update_image_settings(
        self, item: str, image_settings_data: dict[str, int]
    ) -> ImageSettings:
        """Service layer method to create new or update image settings"""
        if not item:
            raise InvalidInputError("Item cannot be empty.")

        self._validate_image_settings_keys(image_settings_data)

        data_condition = {"item": item}

        existing_settings = self.read_image_settings(item)
        if not existing_settings:
            image_settings_data.update(data_condition)
            return self.repo.create_image_settings(image_settings_data)

        return self.repo.update_image_settings(data_condition, image_settings_data)
