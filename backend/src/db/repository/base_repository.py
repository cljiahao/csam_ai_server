import sqlalchemy as sa
from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

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
        conditions = []
        for key, value in filters.items():
            if hasattr(self.model, key):
                conditions.append(getattr(self.model, key) == value)
            else:
                raise AttributeError(
                    f"Model '{self.model.__name__}' has no attribute '{key}'"
                )
        return conditions

    def create(
        self,
        data: dict | list[dict],
        print_message: str = "Error creating data into database.",
    ) -> T | list[T]:
        """Create one or multiple record."""
        try:
            if isinstance(data, list):
                # Bulk create case
                instances = [self.model(**item) for item in data]
                self.db.add_all(instances)
                self.db.commit()
                for instance in instances:
                    self.db.refresh(instance)
                return instances
            else:
                # Single create case
                instance = self.model(**data)
                self.db.add(instance)
                self.db.commit()
                self.db.refresh(instance)
                return instance
        except Exception as e:
            self.db.rollback()
            raise SQLAlchemyError(print_message) from e

    def read(
        self,
        filter_conditions: dict,
        return_all: bool = False,
        print_message: str = "Error reading data from database.",
    ) -> T | list[T]:
        """Read one or multiple record."""
        try:
            if filter_conditions:
                conditions = self._build_filter(filter_conditions)
                statement = sa.select(self.model).filter(sa.and_(*conditions))
                result = self.db.execute(statement)
                if return_all:
                    return result.scalars().all()
                return result.scalars().first()
            else:
                statement = sa.select(self.model)
                result = self.db.execute(statement)
                return result.scalars().all()
        except Exception as e:
            self.db.rollback()
            raise SQLAlchemyError(print_message) from e

    def update(
        self,
        updates_data: dict[str, dict] | list[dict[str, dict]],
        print_message: str = "Error updating data in database.",
    ) -> int | T:
        """Update one or multiple record."""
        try:
            if isinstance(updates_data, dict):
                # Single update case
                missing_key = {"filter_conditions", "update_data"} - updates_data.keys()
                if missing_key:
                    raise KeyError(f"Missing key {missing_key}")
                conditions = self._build_filter(updates_data["filter_conditions"])
                statement = sa.select(self.model).filter(sa.and_(*conditions))
                result = self.db.execute(statement)
                instance = result.scalar_one_or_none()
                if not instance:
                    raise NoResultsFound("No matching record found to update.")
                for key, value in updates_data["update_data"].items():
                    setattr(instance, key, value)
                self.db.commit()
                self.db.refresh(instance)
                return instance
            elif isinstance(updates_data, list):
                # Bulk update case
                count = 0
                for update_item in updates_data:
                    missing_key = {
                        "filter_conditions",
                        "update_data",
                    } - update_item.keys()
                    if missing_key:
                        raise KeyError(f"Missing key {missing_key}")

                    conditions = self._build_filter(update_item["filter_conditions"])
                    statement = (
                        sa.update(self.model)
                        .where(sa.and_(*conditions))
                        .values(**update_item["update_data"])
                    )
                    result = self.db.execute(statement)
                    count += result.rowcount
                self.db.commit()
                self.db.expire_all()
                return count
            else:
                raise ValueError(
                    "Invalid input: updates must be a dict or list of dicts."
                )
        except Exception as e:
            self.db.rollback()
            raise SQLAlchemyError(
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
                    statement = sa.delete(self.model).filter(sa.and_(*conditions))
                    result = self.db.execute(statement)
                    count += result.rowcount
                self.db.commit()
                self.db.expire_all()
                return count
            else:
                # Single delete case
                conditions = self._build_filter(filter_conditions)
                statement = sa.delete(self.model).filter(sa.and_(*conditions))
                result = self.db.execute(statement)
                if result.rowcount == 0:
                    raise NoResultsFound("No record found to delete.")
                self.db.commit()
                self.db.expire_all()
                return result.rowcount
        except Exception as e:
            self.db.rollback()
            raise SQLAlchemyError(
                str(e) if isinstance(e, NoResultsFound) else print_message
            )
