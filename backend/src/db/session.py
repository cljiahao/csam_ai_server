from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import database_settings

# Database URL configuration
SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_settings.LOCAL_DB_PATH}"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[sessionmaker, None, None]:
    """Provide a SQLAlchemy session for dependency injection in FastAPI."""
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
