from typing import Any, Type

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase


Base = declarative_base()

# class Base(DeclarativeBase):
#     id: Any
#     __name__: str

#     @declared_attr
#     def __tablename__(cls: Type["Base"]) -> str:
#         """Generate table name from class name."""
#         return cls.__name__.lower()
