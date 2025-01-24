from sqlalchemy.orm import Session

from core.exceptions import InvalidInputError
from db.models.chip_lot_details import ChipLotDetails
from db.repository.chip_lot_details import ChipLotDetailsRepository


class ChipLotDetailsService:
    def __init__(self, db: Session):
        """Initialize service with repository."""
        self.repo = ChipLotDetailsRepository(db)

    def _validate_filter_conditions(self, filter_conditions: dict) -> None:
        """Validate filter conditions before querying or deleting."""
        if not filter_conditions:
            raise InvalidInputError("Filter conditions cannot be empty.")

        # TODO: Validation

        # keys_list = ["lot_no", "plate_no"]
        # missing_key = [key for key in keys_list if key not in filter_conditions]
        # if missing_key:
        #     raise InvalidInputError(
        #         f"Filter conditions must include {', '.join(missing_key)}."
        #     )

    def _validate_lot_data(self, lot_data: dict):
        """Validate the lot data before creating."""
        if not lot_data:
            raise InvalidInputError("No data provided to create.")

        # required_fields = ["lot_no", "plate_no"]
        # for field in required_fields:
        #     if field not in lot_data:
        #         raise InvalidInputError(f"Missing required field: {field}")

        # if len(lot_data["lot_no"]) != 10:
        #     raise InvalidInputError("Lot number must be 10 characters long.")

    def _validate_update_data(self, update_data: dict):
        """Validate the update data before updating the record."""
        if not update_data:
            raise InvalidInputError("No data provided to update.")

    def create_lot_details(self, lot_data: dict) -> ChipLotDetails:
        """Service layer method to create new lot details."""
        self._validate_lot_data(lot_data)

        return self.repo.create_lot_details(lot_data)

    def read_lot_details(self, filter_conditions: dict) -> ChipLotDetails:
        """Service layer method to read lot details."""
        self._validate_filter_conditions(filter_conditions)

        return self.repo.read_lot_details(filter_conditions)

    def update_lot_details(
        self, filter_conditions: dict, update_data: dict
    ) -> ChipLotDetails:
        """Service layer method to update lot details."""
        self._validate_filter_conditions(filter_conditions)
        self._validate_update_data(update_data)

        return self.repo.update_lot_details(filter_conditions, update_data)

    def delete_lot_details(self, filter_conditions: dict) -> ChipLotDetails:
        """Service layer method to delete lot details."""
        self._validate_filter_conditions(filter_conditions)

        return self.repo.delete_lot_details(filter_conditions)
