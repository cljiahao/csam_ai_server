import os
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Callable, Generator
from unittest.mock import MagicMock

from app import app
from core.directory_manager import directory_manager as dm
from db.base import Base
from db.session import get_db

SQLALCHEMY_DATABASE_URL = f"sqlite:///{dm.base_dir}/tests/test_db.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_database():
    """Create the database tables at the beginning of the test session."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created at session start.")

    yield

    Base.metadata.drop_all(bind=engine)
    engine.dispose()

    if SQLALCHEMY_DATABASE_URL.startswith("sqlite") and os.path.exists(
        SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")
    ):
        os.remove(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", ""))
    print("Database tables dropped at session end.")


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Provide a transactional database session for each test function."""
    transaction = engine.connect()
    transaction.begin()
    session = TestingSession(bind=transaction)

    try:
        yield session
    finally:
        session.close()
        transaction.close()


@pytest.fixture
def test_client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_func_logger(monkeypatch: pytest.MonkeyPatch) -> Callable[[str], MagicMock]:
    """Dynamically mock the logger's error method for testing."""

    def _mock_func_logger(logger_path: str) -> MagicMock:
        """Create a mock for the specified logger path."""
        mock = MagicMock()
        monkeypatch.setattr(logger_path, mock)
        return mock

    return _mock_func_logger


@pytest.fixture
def mock_file_methods() -> tuple[Path, MagicMock]:
    """Fixture to mock file input."""

    mock_file_dir = Path(f"/fake/path/")

    mock_file = MagicMock()
    mock_file.filename = "test_image.png"
    # 1 x 1 Red pixel
    mock_file.file.read.return_value = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00"
        b"\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x16%\x00\x00"
        b"\x16%\x01IR$\xf0\x00\x00\x00\rIDAT\x18Wc\xf8\xcf\xc0\xf0\x1f\x00\x05\x00\x01\xff\xa6\\\x9b]\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    return mock_file_dir, mock_file
