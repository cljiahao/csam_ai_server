from sqlalchemy.orm import Session

from core.exceptions import InvalidInputError
from db.models.chip_lot_details import ChipLotDetails
from db.repository.chip_lot_details import ChipLotDetailsRepository


class ChipLotDetailsService:
    def __init__(self, db: Session):
        """Initialize service with repository."""
        self.repo = ChipLotDetailsRepository(db)

    def _validate_lot_details_keys(self, lot_data: dict) -> None:
        """Validate the keys in the lot details data."""
        valid_keys = {
            "id",
            "item",
            "lot_no",
            "plate_no",
            "with_ai",
            "no_of_chips",
            "no_of_batches",
            "no_of_real",
            "no_of_pred",
        }

        invalid_keys = set(lot_data) - valid_keys
        if invalid_keys:
            raise InvalidInputError(
                f"Unknown keys in lot details data: {', '.join(invalid_keys)}"
            )

    def create_lot_details(self, lot_data: dict) -> ChipLotDetails:
        """Service layer method to create new lot details."""
        self._validate_lot_details_keys(lot_data)

        return self.repo.create_lot_details(lot_data)

    def read_lot_details(self, filter_conditions: dict) -> ChipLotDetails:
        """Service layer method to read lot details."""
        self._validate_lot_details_keys(filter_conditions)

        return self.repo.read_lot_details(filter_conditions)

    def update_lot_details(
        self, filter_conditions: dict, update_data: dict
    ) -> ChipLotDetails:
        """Service layer method to update lot details."""
        self._validate_lot_details_keys(filter_conditions)
        self._validate_lot_details_keys(update_data)

        return self.repo.update_lot_details(
            {"filter_conditions": filter_conditions, "update_data": update_data}
        )
