from sqlalchemy.orm import Session

from db.models.chip_details import ChipDetails
from db.repository.base_repository import BaseRepository


class ChipDetailsRepository(BaseRepository[ChipDetails]):
    def __init__(self, db: Session):
        super().__init__(db, ChipDetails)
        self.db = db

    def bulk_create_chip_details(
        self, bulk_chip_details_data: list[dict]
    ) -> list[ChipDetails]:
        """Bulk create new chip details."""
        return self.create(
            bulk_chip_details_data,
            print_message="Error creating new data into ChipDetails database.",
        )

    def read_all_chip_details(self, filter_conditions: dict) -> list[ChipDetails]:
        """Read all chip details based on filter."""
        return self.read(
            filter_conditions,
            return_all=True,
            print_message="Error reading all data from ChipDetails database.",
        )

    def bulk_update_chip_details(self, update_list: list[dict[str, dict]]) -> int:
        """Bulk update chip details with provided data."""
        return self.update(
            update_list, print_message="Error updating data in BaseSets database."
        )

    def bulk_delete_chip_details(self, filter_conditions: list[dict]) -> int:
        """Bulk delete chip details based on filter."""
        return self.delete(
            filter_conditions,
            print_message=f"Error deleting chip details from the database.",
        )
