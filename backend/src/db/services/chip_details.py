from sqlalchemy.orm import Session

from core.exceptions import InvalidInputError
from db.models.chip_details import ChipDetails
from db.repository.chip_details import ChipDetailsRepository


class ChipDetailsService:
    def __init__(self, db: Session):
        """Initialize service with repository."""
        self.repo = ChipDetailsRepository(db)

    def _validate_filter_conditions(self, filter_conditions: dict) -> None:
        """Validate filter conditions before querying or deleting."""
        if not filter_conditions:
            raise InvalidInputError("Filter conditions cannot be empty.")

        # TODO: Validation

        # keys_list = ["file_name"]
        # missing_key = [key for key in keys_list if key not in filter_conditions]
        # if missing_key:
        #     raise InvalidInputError(
        #         f"Filter conditions must include {', '.join(missing_key)}."
        #     )

    def _validate_chip_data(self, chip_data: dict):
        """Validate the lot data before creating."""
        if not chip_data:
            raise InvalidInputError("No data provided to create.")

        # required_fields = ["file_name"]
        # for field in required_fields:
        #     if field not in chip_data:
        #         raise InvalidInputError(f"Missing required field: {field}")

    def _validate_update_data(self, update_data: dict):
        """Validate the update data before updating the record."""
        if not update_data:
            raise InvalidInputError("No data provided to update.")

    def create_chip_details(self, chip_data: list[dict]) -> list[ChipDetails]:
        """Service layer method to create new lot details."""
        for data in chip_data:
            self._validate_chip_data(data)

        return self.repo.create_bulk_chip_details(chip_data)

    def read_chip_details(self, filter_conditions: dict) -> list[ChipDetails]:
        """Service layer method to read lot details."""
        self._validate_filter_conditions(filter_conditions)

        return self.repo.read_all_chip_details(filter_conditions)

    def update_chip_details(
        self, filter_conditions: list[dict], update_data: list[dict]
    ) -> int:
        """Service layer method to update lot details."""
        for filters in filter_conditions:
            self._validate_filter_conditions(filters)
        for updates in update_data:
            self._validate_update_data(updates)

        return self.repo.update_bulk_chip_details(filter_conditions, update_data)

    def delete_chip_details(self, filter_conditions: list[dict]) -> int:
        """Service layer method to delete lot details."""
        for filters in filter_conditions:
            self._validate_filter_conditions(filters)

        return self.repo.delete_bulk_chip_details(filter_conditions)
