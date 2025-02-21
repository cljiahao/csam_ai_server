import math
from sqlalchemy.orm import Session

from core.exceptions import InvalidInputError
from db.models.image_settings import ImageSettings
from db.repository.image_settings import ImageSettingsRepository


class ImageSettingsService:
    def __init__(self, db: Session):
        """Initialize service with repository."""
        self.repo = ImageSettingsRepository(db)

    @staticmethod
    def _create_filter_conditions(item: str) -> dict[str, str]:
        """Validate filter conditions before querying or deleting."""
        if not item:
            raise InvalidInputError("Filter conditions cannot be empty.")

        return {"item": item}

    @staticmethod
    def _create_settings_dict(
        erode: int, close: int, average_length: int, is_batch: bool
    ) -> dict[str, int | str | bool]:
        """Generate settings dictionary based on batch mode."""
        if is_batch:
            return {"batch_erode": erode, "batch_close": close}

        crop_size = math.ceil(average_length * 2)
        return {
            "chip_erode": erode,
            "chip_close": close,
            "crop_size": crop_size,
        }

    def create_settings(
        self, item: str, erode: int, close: int, average_length: int, is_batch: bool
    ) -> ImageSettings:
        """Service layer method to create new settings."""
        settings_data = self._create_settings_dict(
            erode, close, average_length, is_batch
        )
        settings_data.update({"item": item})

        return self.repo.create_settings(settings_data)

    def read_settings(self, item: str) -> ImageSettings:
        """Service layer method to read settings."""
        filter_condition = self._create_filter_conditions(item)

        return self.repo.read_settings(filter_condition)

    def update_settings(
        self, item: str, erode: int, close: int, average_length: int, is_batch: bool
    ) -> ImageSettings:
        """Service layer method to update settings."""
        filter_condition = self._create_filter_conditions(item)
        update_data = self._create_settings_dict(erode, close, average_length, is_batch)

        return self.repo.update_settings(filter_condition, update_data)

    def delete_settings(self, item: str) -> ImageSettings:
        """Service layer method to delete settings."""
        filter_condition = self._create_filter_conditions(item)

        return self.repo.delete_settings(filter_condition)
