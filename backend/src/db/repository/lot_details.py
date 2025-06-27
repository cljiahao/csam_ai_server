from sqlalchemy.orm import Session

from db.models.lot_details import LotDetails
from db.repository.base_repository import BaseRepository


class LotDetailsRepository(BaseRepository[LotDetails]):
    def __init__(self, db: Session):
        super().__init__(db, LotDetails)

    def create_lot_details(self, lot_data: dict) -> list[LotDetails]:
        """Create new lot details."""
        return self.create(
            lot_data,
            print_message="Error creating new data into LotDetails database.",
        )

    def read_all_lot_details(self, filter_conditions: dict) -> list[LotDetails]:
        """Read all lot details based on filter."""
        return self.read(
            filter_conditions,
            return_all=True,
            print_message="Error reading all data from LotDetails database.",
        )

    def read_lot_details(self, filter_conditions: dict) -> list[LotDetails]:
        """Read lot details based on filter."""
        return self.read(
            filter_conditions,
            print_message="Error reading data from LotDetails database.",
        )

    def update_lot_details(self, update_lists: list[dict[str, dict]]) -> int:
        """Update lot details with provided data."""
        return self.update(
            update_lists,
            print_message="Error updating data in LotDetails database.",
        )

    def delete_lot_details(self, filter_conditions: dict) -> int:
        """Delete lot details based on filter."""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from LotDetails database.",
        )
