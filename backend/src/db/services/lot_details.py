from sqlalchemy.orm import Session

from core.exceptions import InvalidInputError, NoResultsFound
from db.models.lot_details import LotDetails
from db.repository.chip_details import ChipDetailsRepository
from db.repository.lot_details import LotDetailsRepository


class LotDetailsService:
    def __init__(self, db: Session):
        self.lot_details_repo = LotDetailsRepository(db)
        self.chip_details_repo = ChipDetailsRepository(db)

    def _validate_lot_details_data_keys(self, data: dict) -> None:
        """Validate the keys in lot details data."""
        valid_keys = {
            "item",
            "lot_no",
            "plate_no",
            "is_ai",
            "no_of_chips",
            "no_of_batches",
            "no_of_real",
            "no_of_pred",
        }
        invalid_keys = set(data) - valid_keys
        if invalid_keys:
            raise InvalidInputError(
                f"Unknown keys in Lot Details data: {', '.join(invalid_keys)}"
            )

    def _validate_chip_details_data_keys(self, data: dict) -> None:
        """Validate the keys in chip details data."""
        valid_keys = {
            "batch_no",
            "file_name",
            "norm_x_center",
            "norm_y_center",
            "defect_mode",
        }
        invalid_keys = set(data) - valid_keys
        if invalid_keys:
            raise InvalidInputError(
                f"Unknown keys in Chip Details data: {', '.join(invalid_keys)}"
            )

    def read_lot_details_by_id(self, lot_details_id: str) -> LotDetails:
        """Service layer method to read by id"""

        return self.lot_details_repo.read_lot_details(
            {"lot_details_id": lot_details_id}
        )[0]

    def read_lot_details(self, lot_no: str, plate_no: str, is_ai: int) -> LotDetails:
        """Service layer method to read lot details by filter conditions"""
        if not lot_no or not plate_no:
            raise InvalidInputError("Lot No or Plate No cannot be empty")
        if is_ai != 0 and is_ai != 1:
            raise InvalidInputError("is AI flag not boolean type")
        filter_condition = {"lot_no": lot_no, "plate_no": plate_no, "is_ai": is_ai}

        return self.lot_details_repo.read_lot_details(filter_condition)[0]

    def _read_or_create_lot_details(self, lot_data: dict[str, str | int]) -> LotDetails:
        """Read lot details for an item, or create them if they don't exist."""

        self._validate_lot_details_data_keys(lot_data)

        lot_details = self.read_lot_details(
            lot_data["lot_no"], lot_data["plate_no"], lot_data["is_ai"]
        )
        if not lot_details:
            lot_details = self.lot_details_repo.create_lot_details(lot_data)[0]

        return lot_details

    def bulk_create_lot_and_chip_details(
        self,
        chip_details_data_list: list[dict[str, str | int]],
        lot_data: dict[str, str | int],
    ) -> str:
        """Service layer method to bulk create new chip details."""

        for chip_details_data in chip_details_data_list:
            self._validate_chip_details_data_keys(chip_details_data)

        lot_details = self._read_or_create_lot_details(lot_data)
        update_chip_details_with_id = [
            {**chip_details_data, "lot_details_id": lot_details.id}
            for chip_details_data in chip_details_data_list
        ]

        self.chip_details_repo.bulk_create_chip_details(update_chip_details_with_id)
        return lot_details.id

    def bulk_update_chip_details(
        self, chip_details_list: list[dict[str, str | int]]
    ) -> int:
        """Service layer method to update chip details."""
        update_list = []
        for chip_details in chip_details_list:
            self._validate_chip_details_data_keys(chip_details)
            update_list.append(
                {
                    "filter_conditions": {"file_name": chip_details["file_name"]},
                    "update_data": {"defect_mode": chip_details["defect_mode"]},
                }
            )

        return self.chip_details_repo.bulk_update_chip_details(update_list)

    def update_lot_details(self, lot_details_id: str, no_of_real: int) -> int:
        """Service layer method to update lot details."""

        if not self.read_lot_details_by_id(lot_details_id):
            raise NoResultsFound(
                f"LotDetails do not have '{lot_details_id}' in the database."
            )
        if not isinstance(no_of_real, int):
            raise TypeError("no_of_real argument received is not int type.")

        update_list = {
            "filter_conditions": {"id": lot_details_id},
            "update_data": {"no_of_real": no_of_real},
        }

        return self.lot_details_repo.update_lot_details(update_list)
