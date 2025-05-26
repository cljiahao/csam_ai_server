from sqlalchemy.orm import Session

from core.exceptions import InvalidInputError, NoResultsFound
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
            "chip_noise_erode",
            "chip_dilate",
            "chip_erode",
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
        filter_conditions = {"item": item}

        return self.repo.read_image_settings(filter_conditions)[0]

    def read_image_settings_not_empty(self, item: str) -> ImageSettings:
        """Service layer method to read image settings, ensure not empty"""
        image_settings = self.read_image_settings(item)

        if image_settings is None:
            raise NoResultsFound(
                f"Image settings for '{item}' not found in API or database."
            )
        return image_settings

    def create_or_update_image_settings(
        self, item: str, image_settings_data: dict[str, int]
    ) -> ImageSettings | int:
        """Service layer method to create new or update image settings"""
        if not item:
            raise InvalidInputError("Item cannot be empty.")

        self._validate_image_settings_keys(image_settings_data)

        data_condition = {"item": item}

        existing_settings = self.read_image_settings(item)
        if existing_settings:
            if "crop_size" in image_settings_data and existing_settings.crop_size != 0:
                del image_settings_data["crop_size"]

            self.repo.update_image_settings(
                {
                    "filter_conditions": data_condition,
                    "update_data": image_settings_data,
                }
            )
            return self.read_image_settings_not_empty(item)

        image_settings_data.update(data_condition)
        return self.repo.create_image_settings(image_settings_data)[0]
