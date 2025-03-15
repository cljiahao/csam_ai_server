from sqlalchemy.orm import Session

from core.exceptions import InvalidInputError
from db.models.chip_details import ChipDetails
from db.repository.chip_details import ChipDetailsRepository


class ChipDetailsService:
    def __init__(self, db: Session):
        """Initialize service with repository."""
        self.repo = ChipDetailsRepository(db)

    def _validate_chip_details_keys(self, chip_details_data: dict) -> None:
        """Validate the keys in the chip details data."""
        valid_keys = {
            "file_name",
            "defect_mode",
            "chip_lot_id",
            "batch_no",
        }

        invalid_keys = set(chip_details_data) - valid_keys
        if invalid_keys:
            raise InvalidInputError(
                f"Unknown keys in chip details data: {', '.join(invalid_keys)}"
            )

    def bulk_create_chip_details(self, chip_data: list[dict]) -> list[ChipDetails]:
        """Service layer method to bulk create new lot details."""
        for data in chip_data:
            self._validate_chip_details_keys(data)

        return self.repo.bulk_create_chip_details(chip_data)

    def read_all_chip_details(self, filter_conditions: dict) -> list[ChipDetails]:
        """Service layer method to read all lot details based on filter conditions."""
        self._validate_chip_details_keys(filter_conditions)

        return self.repo.read_all_chip_details(filter_conditions)

    def bulk_update_chip_details(self, update_list: list[dict[str, dict]]) -> int:
        """Service layer method to bulk update lot details."""
        for update_item in update_list:
            self._validate_chip_details_keys(update_item["update_data"])

        return self.repo.bulk_update_chip_details(update_list)
