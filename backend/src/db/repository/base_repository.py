from sqlite3 import DatabaseError
from typing import Generic, TypeVar, Type
from sqlalchemy import and_, delete, select, update
from sqlalchemy.orm import Session

from core.exceptions import NoResultsFound

# Define generic types for the model
T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Base repository class to handle CRUD operations.

    Args:
        db: SQLAlchemy session object
        model: SQLAlchemy model class

    Attributes
        db: SQLAlchemy session object
        model: SQLAlchemy model class
    """

    def __init__(self, db: Session, model: Type[T]) -> None:

        self.db = db
        self.model = model

    def _build_filter(self, filters: dict) -> list:
        """Build filter conditions dynamically"""
        if not filters:
            raise ValueError("Filters cannot be empty.")
        conditions = [
            getattr(self.model, key) == value for key, value in filters.items()
        ]
        return conditions

    def create(
        self,
        data: dict | list[dict],
        print_message: str = "Error creating data into database.",
    ) -> T | list[T]:
        """Create one or multiple record."""
        try:
            if isinstance(data, list):
                instances = [self.model(**item) for item in data]
                self.db.add_all(instances)
                self.db.commit()
                for instance in instances:
                    self.db.refresh(instance)
                return instances
            else:
                instance = self.model(**data)
                self.db.add(instance)
                self.db.commit()
                return instance
        except:
            self.db.rollback()
            raise DatabaseError(print_message)

    def read(
        self,
        filter_conditions: dict,
        return_all: bool = False,
        print_message: str = "Error reading data from database.",
    ) -> T | list[T]:
        """Read one or multiple record."""
        try:
            conditions = self._build_filter(filter_conditions)
            statement = select(self.model).filter(and_(*conditions))
            result = self.db.execute(statement)
            if return_all:
                return result.scalars().all()
            return result.scalars().first()
        except:
            self.db.rollback()
            raise DatabaseError(print_message)

    def update(
        self,
        filter_conditions: dict | list[dict],
        update_data: dict | list[dict],
        print_message: str = "Error updating data in database.",
    ) -> int | T:
        """Update one or multiple record."""
        try:
            if isinstance(filter_conditions, dict) and isinstance(update_data, dict):
                # Single update case
                conditions = self._build_filter(filter_conditions)
                statement = select(self.model).filter(and_(*conditions))
                result = self.db.execute(statement)
                instance = result.scalars().first()
                if not instance:
                    raise NoResultsFound("No matching record found to update.")
                for key, value in update_data.items():
                    setattr(instance, key, value)
                self.db.commit()
                self.db.refresh(instance)
                return instance
            elif isinstance(filter_conditions, list):
                # Bulk update case
                count = 0
                for i, filters in enumerate(filter_conditions):
                    conditions = self._build_filter(filters)
                    data = (
                        update_data[i] if isinstance(update_data, list) else update_data
                    )
                    statement = (
                        update(self.model).where(and_(*conditions)).values(**data)
                    )
                    result = self.db.execute(statement)
                    count += result.rowcount
                self.db.commit()
                return count
            else:
                NoResultsFound(
                    "Invalid input of filter_conditions and update_data type."
                )
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(
                str(e) if isinstance(e, NoResultsFound) else print_message
            )

    def delete(
        self,
        filter_conditions: dict | list[dict],
        print_message: str = "Error deleting data from database.",
    ) -> int | T:
        """Delete one or multiple record."""
        try:
            if isinstance(filter_conditions, list):
                # Bulk delete case
                count = 0
                for filters in filter_conditions:
                    conditions = self._build_filter(filters)
                    statement = delete(self.model).filter(and_(*conditions))
                    result = self.db.execute(statement)
                    count += result.rowcount
                self.db.commit()
                return count
            else:
                # Single delete case
                conditions = self._build_filter(filter_conditions)
                statement = select(self.model).filter(and_(*conditions))
                result = self.db.execute(statement)
                instance = result.scalars().first()
                if not instance:
                    raise NoResultsFound("No record found to delete.")
                self.db.delete(instance)
                self.db.commit()
                return instance
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(
                str(e) if isinstance(e, NoResultsFound) else print_message
            )
