from sqlalchemy.orm import Session

from db.models.chip_details import ChipDetails
from db.repository.base_repository import BaseRepository


class ChipDetailsRepository(BaseRepository[ChipDetails]):
    def __init__(self, db: Session):
        super().__init__(db, ChipDetails)
        self.db = db

    def bulk_create_chip_details(self, bulk_chip_data: list[dict]) -> list[ChipDetails]:
        """Create new bulk chip details."""
        return self.create(
            bulk_chip_data,
            print_message=f"Error creating bulk chip details into the database.",
        )

    def read_all_chip_details(self, filter_conditions: dict) -> list[ChipDetails]:
        """Read chip details based on filter."""
        return self.read(
            filter_conditions,
            return_all=True,
            print_message=f"Error reading chip details from the database.",
        )


    def bulk_update_chip_details(self, updates_list: list[dict[str, dict]]) -> int:
        """Update chip details with provided data."""
        return self.update(
            updates_list,
            print_message=f"Error updating bulk chip details in the database.",
            
        )

    def bulk_delete_chip_details(self, filter_conditions: list[dict]) -> int:
        """Update chip details with provided data."""
        return self.delete(
            filter_conditions,
            print_message=f"Error deleting bulk chip details from the database.",
        )
