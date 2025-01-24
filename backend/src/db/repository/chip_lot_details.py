from sqlalchemy.orm import Session

from db.models.chip_lot_details import ChipLotDetails
from db.repository.base_repository import BaseRepository


class ChipLotDetailsRepository(BaseRepository[ChipLotDetails]):
    def __init__(self, db: Session):
        super().__init__(db, ChipLotDetails)

    def create_lot_details(self, lot_data: dict) -> ChipLotDetails:
        """Create new chip lot details."""
        return self.create(
            lot_data,
            print_message=f"Error creating lot details from the database.",
        )

    def read_lot_details(self, filter_conditions: dict) -> ChipLotDetails:
        """Read chip lot details based on filter."""
        return self.read(
            filter_conditions,
            print_message=f"Error reading lot details from the database.",
        )

    def update_lot_details(
        self, filter_conditions: dict, update_data: dict
    ) -> ChipLotDetails:
        """Update lot details with provided data."""
        return self.update(
            filter_conditions,
            update_data,
            print_message=f"Error updating lot details in the database.",
        )

    def delete_lot_details(self, filter_conditions: dict) -> ChipLotDetails:
        """Delete chip lot details based on filter."""
        return self.delete(
            filter_conditions,
            print_message=f"Error deleting lot details from the database.",
        )
